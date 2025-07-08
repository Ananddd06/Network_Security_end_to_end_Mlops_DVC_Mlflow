import os 
import sys
import json

from pymongo import MongoClient
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException

log = Custom_Logger().get_logger()

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    log.error("MONGO_DB_URL is not set in the environment variables. Please check your .env file.")


# class MongoDBConnection: