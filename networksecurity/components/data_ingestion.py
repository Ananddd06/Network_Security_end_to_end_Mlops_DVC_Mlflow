import os 
import sys
import numpy as np
import pandas as pd
from typing import List
from networksecurity.exception.exception import CustomException
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.entity.config_entity import DataIngestionConfigEntity
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split

# from dotenv import load_dotenv
# load_dotenv()

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfigEntity):
        self.data_ingestion_config = data_ingestion_config
        self.logger = Custom_Logger().get_logger()

    def export_data_into_feature_store(self) -> pd.DataFrame:
        try:
            self.logger.info("Exporting data into feature store...")

            os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_file_path), exist_ok=True)

            df: pd.DataFrame = pd.read_csv(self.data_ingestion_config.source_data_file_path)
            self.logger.info(f"Data read from {self.data_ingestion_config.source_data_file_path} successfully.")

            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False)
            self.logger.info(f"Data exported to feature store at {self.data_ingestion_config.feature_store_file_path}.")

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def split_data_into_train_and_test(self, df: pd.DataFrame) -> None:
        try:
            self.logger.info("Splitting data into training and testing sets...")

            train_df, test_df = train_test_split(
                df, 
                test_size=self.data_ingestion_config.train_test_split_ratio, 
                random_state=42
            )
            self.logger.info("Data split into training and testing sets successfully.")

            # ✅ Ensure directories exist
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path), exist_ok=True)

            train_df.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False)
            self.logger.info(f"Training data saved to {self.data_ingestion_config.training_file_path}.")
            self.logger.info(f"Testing data saved to {self.data_ingestion_config.testing_file_path}.")

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.logger.info("Starting data ingestion process...")

            df = self.export_data_into_feature_store()
            self.split_data_into_train_and_test(df)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            self.logger.info("Data ingestion completed successfully.")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)
