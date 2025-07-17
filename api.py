from bson import ObjectId
from database import get_collection

def word_helper(word) -> dict:
    return {
        "id": str(word["_id"]),
        "word": word["word"],
        "shortMeaning": word["shortMeaning"],
        "detailedMeaning": word["detailedMeaning"],
        "wordForms": word["wordForms"],
        "examples": word["examples"],
        "relatedWords": word["relatedWords"]
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