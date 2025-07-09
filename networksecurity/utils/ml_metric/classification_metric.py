import os
import sys
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    r2_score
)

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Calculate classification metrics: precision, recall, f1-score, and r2-score.
    
    Args:
        y_true (list or array): True labels.
        y_pred (list or array): Predicted labels.
    
    Returns:
        ClassificationMetricArtifact: An artifact containing the classification metrics.
    """
    try:
        model_precision = precision_score(y_true, y_pred)
        model_recall = recall_score(y_true, y_pred)
        model_f1 = f1_score(y_true, y_pred)
        model_r2 = r2_score(y_true, y_pred)

        return ClassificationMetricArtifact(
            precision=model_precision,
            recall=model_recall,
            f1_score=model_f1,
            r2_score=model_r2
        )
    except Exception as e:
        raise CustomException(e, sys) from e
