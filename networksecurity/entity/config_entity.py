import os
from networksecurity.constants import training_pipeline
from dataclasses import dataclass
from datetime import datetime

class TrainingPipelineConfigEntity:
    def __init__(self):
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.pipeline_name: str = training_pipeline.PIPELINE_NAME
        self.artifacts_name: str = training_pipeline.ARTIFACTS_DIR
        self.artifact_dir: str = os.path.join(self.artifacts_name, self.pipeline_name, timestamp)
        self.timestamp: str = timestamp

@dataclass
class DataIngestionConfigEntity:
    training_pipeline_config: TrainingPipelineConfigEntity

    def __post_init__(self):
        self.data_ingestion_dir: str = os.path.join(
            self.training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.source_data_file_path: str = training_pipeline.DATA_INGESTION_SOURCE_PATH  # New: path to CSV file
