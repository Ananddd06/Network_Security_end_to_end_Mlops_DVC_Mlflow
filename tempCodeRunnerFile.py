import sys
import os
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_tranformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config_entity import (
    DataIngestionConfigEntity,
    DataValidationConfigEntity,
    DataTransformationConfigEntity,
    TrainingPipelineConfigEntity,
    ModelTrainerConfigEntity
)
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact , DataIngestionArtifact
logger = Custom_Logger().get_logger()

if __name__ == "__main__":
    try:
        # Configurations
        training_pipeline_config = TrainingPipelineConfigEntity()
        data_ingestion_config = DataIngestionConfigEntity(training_pipeline_config=training_pipeline_config)
        data_validation_config = DataValidationConfigEntity(training_pipeline_config=training_pipeline_config)

        # Data Ingestion
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact: DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
        logger.info("✅ Data ingestion completed successfully.")
        logger.info(f"📦 Data Ingestion Artifact: {data_ingestion_artifact}")

        # Data Validation
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_artifact=data_ingestion_artifact,
        )
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("✅ Data validation completed successfully.")
        print(f"📄 Data Validation Artifact: {data_validation_artifact}")

        # Data Transformation
        data_transformation_config = DataTransformationConfigEntity(
            training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_validation_artifact=data_validation_artifact,
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info("✅ Data transformation completed successfully.")
        logger.info(f"📊 Data TransformationArtifact: {data_transformation_artifact}")

        logger.info("Model Training sstared")
        model_trainer_config=ModelTrainerConfigEntity(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logger.info("Model Training artifact created")
    except Exception as e:
        logger.error(f"❌ Unexpected error in main pipeline: {e}")
        raise CustomException(e, sys)
