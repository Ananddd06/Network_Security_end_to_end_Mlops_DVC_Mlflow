from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os , sys

from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException

class NetworkModel:
    def __init__(self, preprocessor , model):
        try:
            self.preprocessor = preprocessor
            self.model = model
            self.logger = Custom_Logger().get_logger()
            self.logger.info("NetworkModel initialized with preprocessor and model.")
            pass
        except Exception as e:
            raise CustomException(e, sys)
    
    def predict(self, X):
        try:
            self.logger.info("Starting prediction process.")
            # Transform the input data using the preprocessor
            X_transformed = self.preprocessor.transform(X)
            self.logger.info("Input data transformed successfully.")
            # Make predictions using the model
            predictions = self.model.predict(X_transformed)
            self.logger.info("Predictions made successfully.")
            return predictions
        except Exception as e:
            raise CustomException(e, sys)