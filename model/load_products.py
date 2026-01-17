import os
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")

def load_products():
    if not MONGO_URI:
        raise ValueError("❌ MONGO_URI not found in .env")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    data = list(collection.find({}, {
        "_id": 0,
        "externalId": 1,
        "name": 1,
        "brand": 1,
        "category": 1,
        "description": 1,
        "price": 1
    }))

    return pd.DataFrame(data)
