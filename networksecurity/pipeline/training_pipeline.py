import os , sys 

from networksecurity.logger.customlogger import CustomLogger
from networksecurity.exception.exception import CustomException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_tranformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfigEntity,
    DataIngestionConfigEntity ,
    DataValidationConfigEntity,
    DataTransformationConfigEntity,
    ModelTrainerConfigEntity
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

logger = CustomLogger().get_logger()

class TrainingPipeline:
    def __init__(self, config: TrainingPipelineConfigEntity):
        self.training_pipeline_config = TrainingPipelineConfigEntity()
    
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logger.info("🚀 Starting data ingestion process...")
            data_ingestion_config = DataIngestionConfigEntity(training_pipeline_config=self.training_pipeline_config)
            # Data Ingestion
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact: DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
            logger.info("✅ Data ingestion completed successfully.")
            logger.info(f"📦 Data Ingestion Artifact: {data_ingestion_artifact}")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logger.info("🚀 Starting data validation process...")
            data_validation_config = DataValidationConfigEntity(training_pipeline_config=self.training_pipeline_config)
            # Data Validation
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,
                                             data_validation_config=data_validation_config)
            data_validation_artifact: DataValidationArtifact = data_validation.initiate_data_validation()
            logger.info("✅ Data validation completed successfully.")
            logger.info(f"📦 Data Validation Artifact: {data_validation_artifact}")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logger.info("🚀 Starting data transformation process...")
            data_transformation_config = DataTransformationConfigEntity(training_pipeline_config=self.training_pipeline_config)
            # Data Transformation
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_transformation_config)
            data_transformation_artifact: DataTransformationArtifact = data_transformation.initiate_data_transformation()
            logger.info("✅ Data transformation completed successfully.")
            logger.info(f"📦 Data TransformationArtifact: {data_transformation_artifact}")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logger.info("🚀 Starting model training process...")
            model_trainer_config = ModelTrainerConfigEntity(training_pipeline_config=self.training_pipeline_config)
            # Model Trainer
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=model_trainer_config)
            model_trainer_artifact: ModelTrainerArtifact = model_trainer.initiate_model_trainer()
            logger.info("✅ Model training completed successfully.")
            logger.info(f"📦 Model Trainer Artifact: {model_trainer_artifact}")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def run_pipeline(self):
        try:
            logger.info("🚀 Starting the training pipeline...")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            logger.info("✅ Training pipeline completed successfully.")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
