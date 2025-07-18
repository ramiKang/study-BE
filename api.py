from bson import ObjectId
from database import get_collection
from openai_service import generate_word_data, validate_word_data
from typing import Dict

def word_helper(word) -> dict:
    return {
        "id": str(word["_id"]),
        "word": word["word"],
        "meaning": word.get("meaning", word.get("shortMeaning")),
        "description": word.get("description", word.get("detailedMeaning")),
        "wordForms": word.get("wordForms"),
        "examples": word["examples"],
        "relatedWords": word.get("relatedWords")
    }

def get_all_words():
    collection = get_collection()
    words = []
    cursor = collection.find({})
    for word in cursor:
        words.append(word_helper(word))
    return words

def create_word(word_data: dict):
    """새 단어 추가"""
    collection = get_collection()
    
    # 중복 단어 체크
    existing_word = collection.find_one({"word": word_data["word"]})
    if existing_word:
        raise ValueError(f"단어 '{word_data['word']}'가 이미 존재합니다.")
    
    result = collection.insert_one(word_data)
    created_word = collection.find_one({"_id": result.inserted_id})
    return word_helper(created_word)


def delete_word(word_id: str):
    """단어 삭제"""
    collection = get_collection()

    # ObjectId 유효성 검사
    if not ObjectId.is_valid(word_id):
        return False

    result = collection.delete_one({"_id": ObjectId(word_id)})
    return result.deleted_count > 0


def create_word_with_ai(word: str) -> Dict:
    """
    OpenAI API를 사용하여 영단어 정보를 생성하고 데이터베이스에 추가합니다.
    
    Args:
        word (str): 영단어
        
    Returns:
        Dict: 생성된 단어 정보 객체
    """
    try:
        # OpenAI API로 단어 데이터 생성
        word_data = generate_word_data(word)
        
        # 데이터 검증
        if not validate_word_data(word_data):
            raise ValueError("생성된 단어 데이터가 올바른 형식이 아닙니다.")
        
        # 데이터베이스에 추가
        created_word = create_word(word_data)
        return created_word
            
    except ValueError as e:
        # 이미 존재하는 단어이거나 데이터 검증 실패
        raise e
    except Exception as e:
        # 기타 오류
        raise ValueError(f"단어 생성 중 오류가 발생했습니다: {str(e)}")