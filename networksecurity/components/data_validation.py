from networksecurity.entity.artifact_entity import DataValidationArtifact , DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys
import yaml

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        self.logger = Custom_Logger().get_logger()

    