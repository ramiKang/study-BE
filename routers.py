from fastapi import APIRouter, HTTPException, status
from typing import List
from models import WordEntry, WordEntryCreate
import api


router = APIRouter()

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
