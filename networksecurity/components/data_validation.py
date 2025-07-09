from networksecurity.entity.artifact_entity import DataValidationArtifact , DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.logger.customlogger import Custom_Logger
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys
import yaml