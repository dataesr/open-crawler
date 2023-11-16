from app.config import settings
from pymongo import MongoClient


client = MongoClient(host=settings.MONGO_URI)
db = None


def init_database():
    global db
    if db is None:
        db = client[settings.MONGO_DBNAME]
        db[settings.MONGO_WEBSITES_COLLECTION].create_index(
            [("id", 1)], unique=True
        )
        db[settings.MONGO_WEBSITES_COLLECTION].create_index(
            [("url", 1)], unique=True
        )
        db[settings.MONGO_CRAWLS_COLLECTION].create_index([("id", 1)], unique=True)
