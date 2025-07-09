import sys , os 
import numpy as np 
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from networksecurity.exception.exception import CustomException
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS , TARGET_COLUMN
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact , 
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfigEntity
from networksecurity.utils.main_utils import save_numpy_array_data , save_obj



class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfigEntity, data_validation_artifact: DataValidationArtifact):
        self.data_transformation_config : DataTransformationConfigEntity = data_transformation_config
        self.data_validation_artifact : DataValidationArtifact = data_validation_artifact
        self.logger = Custom_Logger().get_logger()
        self.logger.info("Data Transformation class initialized.")
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys) from e
    def get_data_transformation_pipeline(self) -> Pipeline:
        """
        Creates a data transformation pipeline with KNNImputer and StandardScaler.
        """
        try:
            self.logger.info("Creating data transformation pipeline.")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprcessor : Pipeline = Pipeline(steps=[("imputer", imputer)])
            self.logger.info("Data transformation pipeline created successfully.")
            return preprcessor
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        self.logger.info("Entered initiate_data_transformation method of DataTransformation class.")
        try:
            self.logger.info("Reading training and testing data.")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            self.logger.info("Data read successfully. Starting preprocessing.")

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1 , 0)
            self.logger.info("Training data split into input and target features.")

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1 , 0)
            self.logger.info("Testing data split into input and target features.")

            preprocessor = self.get_data_transformation_pipeline()
            self.logger.info("Data transformation pipeline created successfully.")
            # Fit the preprocessor on the training data
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # save the numpy arrays
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_obj(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_object)
            self.logger.info("Transformed data saved successfully.")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            self.logger.info("Data transformation artifact created successfully.")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) 
    
