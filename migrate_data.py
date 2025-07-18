#!/usr/bin/env python3
"""
데이터베이스 마이그레이션 스크립트
기존 shortMeaning, detailedMeaning 필드를 meaning, description으로 변경
"""

from database import connect_to_mongo, close_mongo_connection, get_collection
from pymongo import UpdateOne


def migrate_data():
    """기존 데이터를 새로운 스키마로 마이그레이션"""
    print("데이터베이스 마이그레이션 시작...")
    
    # MongoDB 연결
    connect_to_mongo()
    collection = get_collection()
    
    # 마이그레이션이 필요한 문서 찾기
    documents_to_migrate = list(collection.find({
        "$or": [
            {"shortMeaning": {"$exists": True}},
            {"detailedMeaning": {"$exists": True}}
        ]
    }))
    
    if not documents_to_migrate:
        print("마이그레이션이 필요한 문서가 없습니다.")
        close_mongo_connection()
        return
    
    print(f"마이그레이션 대상 문서 수: {len(documents_to_migrate)}")
    
    # 배치 업데이트를 위한 operations 리스트
    operations = []
    
    for doc in documents_to_migrate:
        update_fields = {}
        unset_fields = {}
        
        # shortMeaning -> meaning
        if "shortMeaning" in doc:
            update_fields["meaning"] = doc["shortMeaning"]
            unset_fields["shortMeaning"] = ""
        
        # detailedMeaning -> description
        if "detailedMeaning" in doc:
            update_fields["description"] = doc["detailedMeaning"]
            unset_fields["detailedMeaning"] = ""
        
        # 업데이트 연산 생성
        update_operation = {}
        if update_fields:
            update_operation["$set"] = update_fields
        if unset_fields:
            update_operation["$unset"] = unset_fields
        
        if update_operation:
            operations.append(
                UpdateOne(
                    {"_id": doc["_id"]},
                    update_operation
                )
            )
    
    # 배치 실행
    if operations:
        result = collection.bulk_write(operations)
        print(f"마이그레이션 완료: {result.modified_count}개 문서 업데이트됨")
    else:
        print("업데이트할 문서가 없습니다.")
    
    # 마이그레이션 결과 확인
    migrated_count = collection.count_documents({"meaning": {"$exists": True}})
    old_fields_count = collection.count_documents({
        "$or": [
            {"shortMeaning": {"$exists": True}},
            {"detailedMeaning": {"$exists": True}}
        ]
    })
    
    print(f"마이그레이션 후 통계:")
    print(f"- meaning 필드가 있는 문서: {migrated_count}개")
    print(f"- 기존 필드가 남아있는 문서: {old_fields_count}개")
    
    close_mongo_connection()
    print("마이그레이션 완료!")


if __name__ == "__main__":
    migrate_data()