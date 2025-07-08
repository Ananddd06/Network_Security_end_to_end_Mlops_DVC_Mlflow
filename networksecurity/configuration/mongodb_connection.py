import os 
import sys
import json

import certifi
import pandas as pd
import numpy as np 
import pymongo
from pymongo import MongoClient
from networksecurity.logger.customlogger import Custom_Logger
from networksecurity.exception.exception import CustomException

log = Custom_Logger().get_logger()

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    log.error("MONGO_DB_URL is not set in the environment variables. Please check your .env file.")

ca = certifi.where()

class MongoDBConnection:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(f"Error initializing MongoDBConnection: {str(e)}", sys)
    
    def cv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient="records")  # <-- This is correct for MongoDB
            return records
        except Exception as e:
            raise CustomException(f"Error converting CSV to JSON: {str(e)}", sys)
    
    def insert_data_to_mongodb(self, records, database , collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            print("Number of records to insert:", len(self.records))
            if self.records:
                print("Sample record:", self.records[0])
            else:
                print("No records to insert!")

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            log.info(f"Data inserted successfully into {self.database.name}.{self.collection.name}")
            return (len(self.records))
        except Exception as e:
            raise CustomException(f"Unexpected error: {str(e)}", sys)

if __name__ == "__main__":
    FILE_PATH = "/Users/anand/Desktop/Network_Security_End_to_End_mlops_DVC_Dagshub/Network_Data/phisingData.csv"
    DATABASE = "network_security" # <-- use the existing database name, all lowercase
    COLLECTION = "NetworkData"
    networkobj = MongoDBConnection()
    records = networkobj.cv_to_json_converter(FILE_PATH)
    inserted_count = networkobj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    log.info(f"Inserted {inserted_count} records into MongoDB collection {COLLECTION} in database {DATABASE}.")