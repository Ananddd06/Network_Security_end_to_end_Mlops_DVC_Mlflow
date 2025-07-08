import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config_entity import DataIngestionConfigEntity
from networksecurity.entity.config_entity import TrainingPipelineConfigEntity

if __name__ == "__main__":
    try:
        # Initialize configuration
        training_pipeline_config = TrainingPipelineConfigEntity()
        data_ingestion_config = DataIngestionConfigEntity(training_pipeline_config=training_pipeline_config)

        # Create Data Ingestion instance
        data_ingestion = DataIngestion(data_ingestion_config)

        # Start data ingestion process
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # Log the artifact paths
        logger = Custom_Logger().get_logger()
        logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

    except CustomException as e:
         raise CustomException(e, sys)