import os
import sys
import numpy as np
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from networksecurity.utils.ml_metric.classification_metric import get_classification_score
from networksecurity.entity.config_entity import ModelTrainerConfigEntity, DataTransformationConfigEntity
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.utils.main_utils import save_obj, load_obj, load_numpy_array_data, evaluate_models
from networksecurity.utils.model_metric.estimator import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

import mlflow
import dagshub
dagshub.init(repo_owner='Ananddd06', repo_name='Network_Security_end_to_end_Mlops_DVC_Mlflow', mlflow=True)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfigEntity,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.logger = Custom_Logger().get_logger()
            self.logger.info("Model Trainer initialized with configuration and artifacts.")
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def track_mlflow(self, model, classification_metric):
        """
        Track the model and its metrics using MLflow.
        
        Args:
            model: The trained model to log.
            classification_metric: The classification metrics to log.
        """
        try:
            self.logger.info("Starting MLflow tracking.")
            # mlflow.set_experiment(experiment_name="Network Security Model Training")
            with mlflow.start_run():
                mlflow.log_metric("precision", classification_metric.precision)
                mlflow.log_metric("recall", classification_metric.recall)
                mlflow.log_metric("f1_score", classification_metric.f1_score)
                mlflow.log_metric("r2_score", classification_metric.r2_score)
                self.logger.info("MLflow tracking completed successfully.")
        except Exception as e:
            raise CustomException(e, sys)
    
    def train_model(self, X_train, y_train, X_test, y_test) -> ModelTrainerArtifact:
        try:
            self.logger.info("Starting model training process.")
            
            models = {
                'Logistic Regression': LogisticRegression(),
                'Random Forest': RandomForestClassifier(),
                'Gradient Boosting': GradientBoostingClassifier(),
                'AdaBoost': AdaBoostClassifier(),
                'Decision Tree': DecisionTreeClassifier(),
                'KNeighbors': KNeighborsClassifier()
            }

            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    'learning_rate': [0.1, 0.01, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }
            
            model_report = {}
            
            for model_name, model in models.items():
                self.logger.info(f"Training and tuning {model_name}...")
                
                param_grid = params.get(model_name, {})
                
                if param_grid:
                    grid_search = GridSearchCV(
                        estimator=model,
                        param_grid=param_grid,
                        cv=3,
                        verbose=3,     # <-- This enables detailed terminal output during fitting
                        n_jobs=-1,
                        scoring='f1'
                    )
                    grid_search.fit(X_train, y_train)
                    best_model = grid_search.best_estimator_
                    best_score = grid_search.best_score_
                    self.logger.info(f"{model_name} best params: {grid_search.best_params_}")
                else:
                    model.fit(X_train, y_train)
                    best_model = model
                    best_score = model.score(X_train, y_train)
                
                model_report[model_name] = best_score
                models[model_name] = best_model  # update with best estimator
            
            self.logger.info("Model evaluation completed.")
            
            # Select best model based on score
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]

            self.logger.info(f"Best model selected: {best_model_name} with score: {best_model_score}")

            # Final training predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            self.track_mlflow(best_model, classification_train_metric)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            preprocessor = load_obj(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_obj(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

            save_obj(file_path="final_model/model.pkl", obj=best_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                trained_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            self.logger.info(f"ModelTrainerArtifact created: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Load transformed data arrays
            train_arr = load_numpy_array_data(file_path=train_file_path)
            test_arr = load_numpy_array_data(file_path=test_file_path)

            # Split features and target
            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            self.logger.info("Loaded and split training and testing data successfully.")
            
            # Start training
            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
            
            self.logger.info("Model training completed successfully.")
            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e, sys)
