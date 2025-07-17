from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

# 환경 변수 로드
load_dotenv()

uri = os.getenv("MONGODB_URL")

client = MongoClient(uri)
DATABASE_NAME = "Wordbook"
COLLECTION_NAME = "test-word"

# 전역 변수
client = None
db = None
collection = None


def connect_to_mongo():
    """MongoDB에 연결"""
    global client, db, collection

    try:
        client = MongoClient(uri)

        # 연결 테스트
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        # 데이터베이스와 컬렉션 설정
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        print("=========================")
        print(collection)
        print("=========================")


    except Exception as e:
        print(f"연결 실패: {e}")
        raise


def close_mongo_connection():
    """MongoDB 연결 종료"""
    if client:
        client.close()
        print("MongoDB 연결 종료")


def get_collection():
    """컬렉션 반환"""
    return collection

