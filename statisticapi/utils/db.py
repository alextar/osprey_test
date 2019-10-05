def get_connection():
    from pymongo import MongoClient
    client = MongoClient('mongo')
    db = client.imagedb
    return db