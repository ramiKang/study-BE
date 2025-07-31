from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

load_dotenv()

uri = os.getenv("MONGODB_URL")

DATABASE_NAME = "Wordbook"
COLLECTION_NAME = "words"

client = None
db = None
collection = None


def connect_to_mongo():
    global client, db, collection

    try:
        client = MongoClient(uri)

        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        print("=========================")
        print(collection)
        print("=========================")

    except Exception as e:
        print(f"연결 실패: {e}")
        raise


def close_mongo_connection():
    if client:
        client.close()
        print("MongoDB 연결 종료")


def get_collection():
    return collection