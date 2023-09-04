import os
from pymongo import MongoClient

client = MongoClient(host=os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DBNAME"]]

db[os.environ["MONGO_WEBSITES_COLLECTION"]
   ].create_index([('id', 1)], unique=True)
db[os.environ["MONGO_WEBSITES_COLLECTION"]
   ].create_index([('url', 1)], unique=True)
db[os.environ["MONGO_CRAWLS_COLLECTION"]
   ].create_index([('id', 1)], unique=True)
