import os
import sys
import numpy as np 
import dill
import yaml
from pandas import DataFrame
from networksecurity.exception.exception import CustomException
from networksecurity.logger.customlogger import Custom_Logger
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score

logging = Custom_Logger().get_logger()
def read_yaml_file(file_path: str) -> dict:
    """Reads a YAML file and returns its content as a dictionary."""
    try:
        with open(file_path, 'r') as file:  # Open the file in text mode ('r')
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e, sys) from e

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """Writes content to a YAML file, with an option to replace existing file."""
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Creating directories if not exist
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, 'w') as file:  # Open the file in text mode ('w')
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys) from e

def load_obj(file_path: str) -> object:
    """Loads a pickled object from a file."""
    logging.info("Entered the load object method of Utils")
    try:
        with open(file_path, 'rb') as file:  # Open the file in binary mode ('rb')
            obj = dill.load(file)
            logging.info("Exited the load object from the method utils")
            return obj
    except Exception as e:
        raise CustomException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """Saves a numpy array to a file."""
    try:
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, "wb") as file:  # Open the file in binary mode ('wb')
            np.save(file, array)
    except Exception as e:
        raise CustomException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """Loads a numpy array from a file."""
    try:
        with open(file_path, "rb") as file:  # Open the file in binary mode ('rb')
            return np.load(file)
    except Exception as e:
        raise CustomException(e, sys) from e

def save_obj(file_path: str, obj: object) -> None:
    """Saves an object to a file using dill."""
    logging.info("Enter the save method object of the utils")
    try:
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, "wb") as file:  # Open the file in binary mode ('wb')
            dill.dump(obj, file)

        logging.info("Exited the save object from the utils")
    except Exception as e:
        raise CustomException(e, sys) from e

def drop_columns(df: DataFrame, cols: list) -> DataFrame:
    """Drops specified columns from a DataFrame."""
    logging.info("Entered drop column of the Utils")
    try:
        result = df.drop(cols, axis=1)
        logging.info("Exited the drop columns of the method Utils")
        return result
    except Exception as e:
        raise CustomException(e, sys) from e

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}

        for model_name, model in models.items():
            model_params = params.get(model_name, {})
            gs = GridSearchCV(model, model_params, cv=3) if model_params else None
            
            if gs:
                gs.fit(X_train, y_train)
                best_model = gs.best_estimator_
            else:
                model.fit(X_train, y_train)
                best_model = model

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)
            
            # For classification, consider using accuracy or f1_score instead of r2_score
            train_model_score = accuracy_score(y_train, y_train_pred)
            test_model_score = accuracy_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys) from e
