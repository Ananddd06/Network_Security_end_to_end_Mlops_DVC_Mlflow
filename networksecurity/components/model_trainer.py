import os , sys
import numpy as np
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from networksecurity.utils.ml_metric.classification_metric import get_classification_score
from networksecurity.entity.config_entity import ModelTrainerConfigEntity , DataTransformationConfigEntity
from networksecurity.entity.artifact_entity import DataTransformationArtifactEntity , ModelTrainerArtifactEntity
from networksecurity.utils.main_utils import save_obj , load_obj , load_numpy_array_data , evaluate_models
from networksecurity.utils.model_metric.estimator import NetworkModel
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier , AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklear.neighbors import KNeighborsClassifier


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfigEntity,
                 data_transformation_artifact: DataTransformationArtifactEntity):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.logger = Custom_Logger().get_logger()
            self.logger.info("Model Trainer initialized with configuration and artifacts.")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def train_model(self,X_train , y_train , X_test , y_test) -> NetworkModel:
        try:
            self.logger.info("Starting model training process.")
            models = {
                'LogisticRegression': LogisticRegression(),
                'RandomForestClassifier': RandomForestClassifier(),
                'GradientBoostingClassifier': GradientBoostingClassifier(),
                'AdaBoostClassifier': AdaBoostClassifier(),
                'DecisionTreeClassifier': DecisionTreeClassifier(),
                'KNeighborsClassifier': KNeighborsClassifier()
            }

            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
            
            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=params)
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def initiate_model_trainer(self) -> ModelTrainerArtifactEntity:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Load the transformed train and test data
            train_arr = load_numpy_array_data(file_path=train_file_path)
            test_arr = load_numpy_array_data(file_path=test_file_path)
            pass
            # Split the data into features and target variable
            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]
            self.logger.info("Data loaded and split into features and target variable.")

            model = self.train_model(X_train, y_train)
            self.logger.info("Model trained successfully.")
        except Exception as e:
            raise CustomException(e, sys) 