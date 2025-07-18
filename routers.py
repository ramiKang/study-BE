from fastapi import APIRouter, HTTPException, status
from typing import List
from models import WordEntry, WordEntryCreate
from pydantic import BaseModel
import api


router = APIRouter()

class WordGenerateRequest(BaseModel):
    word: str

@router.get("/words", response_model=List[WordEntry])
async def get_all_words():
    """1. 전체 데이터를 가져오는 API"""
    try:
        return api.get_all_words()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터 조회 중 오류: {str(e)}"
        )

@router.post("/words", response_model=WordEntry, status_code=status.HTTP_201_CREATED)
async def create_word(word_data: WordEntryCreate):
    """2. 데이터를 추가하는 API"""
    try:
        return api.create_word(word_data.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"단어 추가 중 오류: {str(e)}"
        )

@router.delete("/words/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(word_id: str):
    """3. 데이터를 삭제하는 API"""
    try:
        success = api.delete_word(word_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="삭제할 단어를 찾을 수 없습니다."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"단어 삭제 중 오류: {str(e)}"
        )


@router.post("/words/generate", response_model=WordEntry, status_code=status.HTTP_201_CREATED)
async def generate_word_with_ai(request: WordGenerateRequest):
    """4. OpenAI API를 사용하여 영단어 정보를 자동 생성하고 추가하는 API"""
    try:
        result = api.create_word_with_ai(request.word)
        return result
    except ValueError as e:
        # 중복 단어이거나 데이터 검증 실패
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"단어 생성 중 오류: {str(e)}"
        )
