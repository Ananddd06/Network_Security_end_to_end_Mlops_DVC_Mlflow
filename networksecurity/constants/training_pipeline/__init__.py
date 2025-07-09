import os 
import sys 
import numpy as np 
import pandas as pd

"""
Defining common constants for the training pipeline.
"""
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurityTrainingPipeline"
ARTIFACTS_DIR: str = "artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
MODEL_FILE_NAME: str = "model.pkl"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
MODEL_FILE_PATH: str = os.path.join("config", "model.yaml")

"""
Data ingestion related constants
Reading directly from the local CSV file
"""

ROOT_DIR = os.getcwd()  # Gets the current project root
DATA_INGESTION_SOURCE_PATH: str = os.path.join(ROOT_DIR, "Network_Data", FILE_NAME)
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data validation related constants starts with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "valid"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "drift_report.html"
DATA_VALIDATION_DRIFT_SUMMARY_FILE_NAME = "drift_summary.yaml" 

"""
Data transformation related constants
"""
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR : str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR : str = "transformed_object"

DATA_TRANSFORMATION_IMPUTER_PARAMS : dict = {
    "missing_values": np.nan,
    "n-neighbors": 3,
    "weights": "uniform",
}
