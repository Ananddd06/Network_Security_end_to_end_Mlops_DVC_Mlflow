from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

import pandas as pd
import os, sys

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.logger = Custom_Logger().get_logger()
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """Reads data from a file and returns it as a DataFrame."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """Validates the number of columns in the DataFrame against the schema."""
        try:
            expected_columns = self._schema_config['columns']
            actual_columns = dataframe.columns.tolist()

            self.logger.info(f"Expected columns: {expected_columns}")
            self.logger.info(f"Actual columns: {actual_columns}")

            if len(actual_columns) != len(expected_columns):
                self.logger.critical(f"❌ Column mismatch: Expected {len(expected_columns)}, got {len(actual_columns)}")
                return False
            return True
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_data_drift_report(self, train_df: pd.DataFrame, test_df: pd.DataFrame, html_path: str, yaml_path: str = None):
        """Generates a data drift report using Evidently (HTML + optional YAML)."""
        try:
            self.logger.info("📊 Generating data drift report...")

            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=train_df, current_data=test_df)

            report.save_html(html_path)
            self.logger.info(f"✅ Drift report saved: {html_path}")

            # If YAML path is given, save the summary
            if yaml_path:
                result_dict = report.as_dict()
                drift_result = result_dict["metrics"][0]["result"]

                summary = {
                    "drift_detected": drift_result["dataset_drift"],
                    "drifted_feature_count": drift_result["number_of_drifted_columns"],
                    "total_feature_count": drift_result["number_of_columns"],
                    "drift_share": drift_result["share_of_drifted_columns"],
                    "drifted_features": drift_result.get("drifted_columns", [])
                }

                write_yaml_file(yaml_path, summary)
                self.logger.info(f"📄 Drift summary saved to YAML: {yaml_path}")

        except Exception as e:
            self.logger.error("❌ Drift report generation failed.")
            raise CustomException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """Runs the complete data validation pipeline."""
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)
            self.logger.info("✅ Train and test data loaded successfully.")

            # Validate schema for both
            if not self.validate_number_of_columns(train_df):
                raise ValueError("Train data schema mismatch.")
            if not self.validate_number_of_columns(test_df):
                raise ValueError("Test data schema mismatch.")

            # Drift Report (HTML + YAML)
            drift_html = self.data_validation_config.drift_report_path
            drift_yaml = self.data_validation_config.drift_yaml_path

            self.get_data_drift_report(train_df, test_df, drift_html, drift_yaml)

            return DataValidationArtifact(
                validation_status=True,
                drift_report_file_path=drift_html,
                drift_summary_file_path=drift_yaml
            )

        except Exception as e:
            raise CustomException(e, sys) from e
