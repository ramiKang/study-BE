from bson import ObjectId
from app.core.database import get_collection
from app.services.openai_service import generate_word_data, validate_word_data
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
    collection = get_collection()
    
    existing_word = collection.find_one({"word": word_data["word"]})
    if existing_word:
        raise ValueError(f"단어 '{word_data['word']}'가 이미 존재합니다.")
    
    result = collection.insert_one(word_data)
    created_word = collection.find_one({"_id": result.inserted_id})
    return word_helper(created_word)


def delete_word(word_id: str):
    collection = get_collection()

    if not ObjectId.is_valid(word_id):
        return False

    result = collection.delete_one({"_id": ObjectId(word_id)})
    return result.deleted_count > 0


def create_word_with_ai(word: str) -> Dict:
    try:
        word_data = generate_word_data(word)
        
        if not validate_word_data(word_data):
            raise ValueError("생성된 단어 데이터가 올바른 형식이 아닙니다.")
        
        created_word = create_word(word_data)
        return created_word
            
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"단어 생성 중 오류가 발생했습니다: {str(e)}")