from core.config import DB_NAME
from pymongo import MongoClient


def get_connection():
    client = MongoClient('mongo')
    db = client[DB_NAME]
    return db