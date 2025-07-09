import os
import sys
import pandas as pd
import yaml
from scipy.stats import ks_2samp  # Import KS test
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfigEntity
from networksecurity.exception.exception import CustomException
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfigEntity,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.logger = Custom_Logger().get_logger()

            # Create data validation artifact directory if not exists
            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            # Create separate directories for valid train and test data
            self.valid_train_dir = os.path.join(self.data_validation_config.data_validation_dir, "valid_train")
            self.valid_test_dir = os.path.join(self.data_validation_config.data_validation_dir, "valid_test")
            os.makedirs(self.valid_train_dir, exist_ok=True)
            os.makedirs(self.valid_test_dir, exist_ok=True)

            self.logger.info(f"Data validation artifact directory created at {self.data_validation_config.data_validation_dir}")
            self.logger.info(f"Valid train data directory created at {self.valid_train_dir}")
            self.logger.info(f"Valid test data directory created at {self.valid_test_dir}")
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = [list(col_dict.keys())[0] for col_dict in self._schema_config['columns']]
            actual_columns = dataframe.columns.tolist()

            self.logger.info(f"✅ Expected Columns: {expected_columns}")
            self.logger.info(f"🧾 Actual Columns: {actual_columns}")

            if len(actual_columns) != len(expected_columns):
                self.logger.error(f"❌ Column count mismatch: Expected {len(expected_columns)}, got {len(actual_columns)}")
                return False

            missing_cols = [col for col in expected_columns if col not in actual_columns]
            if missing_cols:
                self.logger.error(f"❌ Missing columns in data: {missing_cols}")
                return False

            return True
        except Exception as e:
            raise CustomException(e, sys) from e

    def detect_outliers(self, dataframe: pd.DataFrame) -> dict:
        try:
            self.logger.info("🔍 Detecting outliers using IQR method...")
            outlier_summary = {}
            numeric_columns = dataframe.select_dtypes(include=['int64', 'float64']).columns

            for col in numeric_columns:
                Q1 = dataframe[col].quantile(0.25)
                Q3 = dataframe[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = dataframe[(dataframe[col] < lower_bound) | (dataframe[col] > upper_bound)]
                outlier_count = outliers.shape[0]
                outlier_summary[col] = outlier_count

                self.logger.info(f"📉 Outliers in '{col}': {outlier_count}")

            return outlier_summary
        except Exception as e:
            raise CustomException(e, sys) from e

    def save_outliers_report(self, outliers_before: dict, outliers_after: dict) -> None:
        try:
            outliers_before_path = os.path.join(self.data_validation_config.data_validation_dir, "outliers_before.yml")
            outliers_after_path = os.path.join(self.data_validation_config.data_validation_dir, "outliers_after.yml")

            with open(outliers_before_path, "w") as f_before:
                yaml.dump(outliers_before, f_before)
            self.logger.info(f"Outliers before handling saved at {outliers_before_path}")

            with open(outliers_after_path, "w") as f_after:
                yaml.dump(outliers_after, f_after)
            self.logger.info(f"Outliers after handling saved at {outliers_after_path}")

        except Exception as e:
            raise CustomException(e, sys) from e

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                # KS test
                ks_test_result = ks_2samp(d1, d2)

                drift_detected = ks_test_result.pvalue < threshold
                if drift_detected:
                    status = False

                report[column] = {
                    "p_value": float(ks_test_result.pvalue),
                    "drift_status": drift_detected
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)
            self.logger.info(f"Drift report saved at {drift_report_file_path}")

            return status
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            self.logger.info("📂 Train and Test datasets loaded successfully.")

            if not self.validate_number_of_columns(train_df):
                raise ValueError("❌ Train data columns do not match schema.")
            if not self.validate_number_of_columns(test_df):
                raise ValueError("❌ Test data columns do not match schema.")

            train_outliers_before = self.detect_outliers(train_df)
            test_outliers_before = self.detect_outliers(test_df)
            self.logger.info(f"📊 Train Outliers Before Handling: {train_outliers_before}")
            self.logger.info(f"📊 Test Outliers Before Handling: {test_outliers_before}")

            # TODO: Add your outlier handling here (removal/capping)
            train_df_after = train_df.copy()
            test_df_after = test_df.copy()

            train_outliers_after = self.detect_outliers(train_df_after)
            test_outliers_after = self.detect_outliers(test_df_after)
            self.logger.info(f"📊 Train Outliers After Handling: {train_outliers_after}")
            self.logger.info(f"📊 Test Outliers After Handling: {test_outliers_after}")

            self.save_outliers_report(
                outliers_before={"train": train_outliers_before, "test": test_outliers_before},
                outliers_after={"train": train_outliers_after, "test": test_outliers_after},
            )

            # Detect drift between train and test sets
            drift_status = self.detect_dataset_drift(base_df=train_df_after, current_df=test_df_after)
            self.logger.info(f"⚠️ Dataset drift detected: {not drift_status}")

            # Save valid data files
            valid_train_file_path = os.path.join(self.valid_train_dir, "train.csv")
            valid_test_file_path = os.path.join(self.valid_test_dir, "test.csv")
            train_df_after.to_csv(valid_train_file_path, index=False)
            test_df_after.to_csv(valid_test_file_path, index=False)
            self.logger.info(f"✅ Valid train data saved at {valid_train_file_path}")
            self.logger.info(f"✅ Valid test data saved at {valid_test_file_path}")

            # Return artifact with drift report and summary file paths
            return DataValidationArtifact(
                validation_status=True,
                valid_train_file_path=valid_train_file_path,
                valid_test_file_path=valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                drift_summary_file_path=None  # Add if you have a summary path
            )

        except Exception as e:
            raise CustomException(e, sys) from e
