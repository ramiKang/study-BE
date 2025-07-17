from bson import ObjectId
from database import get_collection

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