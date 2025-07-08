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
