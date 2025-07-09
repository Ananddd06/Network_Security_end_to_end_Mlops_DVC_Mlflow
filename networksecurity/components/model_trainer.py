import os , sys
import numpy as np
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from networksecurity.utils.ml_metric.classification_metric import get_classification_score
from networksecurity.entity.config_entity import ModelTrainerConfigEntity , DataTransformationConfigEntity
from networksecurity.entity.artifact_entity import DataTransformationArtifactEntity , ModelTrainerArtifactEntity
from networksecurity.utils.main_utils import save_obj , load_obj , load_numpy_array_data
from networksecurity.utils.model_metric.estimator import NetworkModel

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfigEntity,
                 data_transformation_config: DataTransformationConfigEntity,
                 data_transformation_artifact: DataTransformationArtifactEntity):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_config = data_transformation_config
            self.data_transformation_artifact = data_transformation_artifact
            self.logger = Custom_Logger().get_logger()
            self.logger.info("Model Trainer initialized with configuration and artifacts.")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifactEntity:
        try:
           pass
        except Exception as e:
            raise CustomException(e, sys) 