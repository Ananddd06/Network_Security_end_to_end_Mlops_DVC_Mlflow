from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env file

uri = os.getenv("MONGO_DB_URL")

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)