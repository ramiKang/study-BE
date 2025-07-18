from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

import api
from database import connect_to_mongo, close_mongo_connection, get_collection
from routers import router

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    yield
    close_mongo_connection()

app = FastAPI(
    title="단어 학습 API",
    description="MongoDB를 활용한 단어 학습 CRUD API",
    version="1.0.0",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "단어 학습 API에 오신 것을 환영합니다! 🚀"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/test-db")
async def test_db():
    collection = get_collection()
    count = collection.count_documents({})
    return {"message": "MongoDB 연결 성공!", "document_count": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)