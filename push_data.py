import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL_KEY")

print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pymongo

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_to_monogdb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    FILE_PATH = "Newtork_data/phisingData.csv"
    DATABASE = "ai_ml"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()
    RECORDS = networkobj.csv_to_json(file_path=FILE_PATH)
    print(RECORDS)
    no_of_records = networkobj.insert_data_to_monogdb(records=RECORDS,database=DATABASE,collection=COLLECTION)

    print("Records : ",no_of_records)

