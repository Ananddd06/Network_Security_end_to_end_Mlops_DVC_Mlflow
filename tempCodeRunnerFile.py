import sys
import os

# --- Debug Info ---
print("--- Debug Info ---")
print("Python Executable:", sys.executable)
print("Python Path (sys.path):")
for p in sys.path:
    print(f"  - {p}")
print("Current Working Directory (os.getcwd()):", os.getcwd())
print("------------------")
# --- End Debug Info ---

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config_entity import (
    DataIngestionConfigEntity,
    DataValidationConfigEntity,
    TrainingPipelineConfigEntity,
)
from networksecurity.entity.artifact_entity import DataIngestionArtifact

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

    except CustomException as e:
        logger.error(f"❌ Custom error in main pipeline: {e}")
        raise e
    except Exception as e:
        logger.error(f"❌ Unexpected error in main pipeline: {e}")
        raise CustomException(e, sys)
