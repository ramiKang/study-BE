from openai import OpenAI
import json
import os
from typing import Dict, List

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_word_data(word: str) -> Dict:
    prompt = f"""
    주어진 영어 단어 '{word}'에 대한 정보를 JSON 형태로 생성해주세요.
    
    다음 형식을 따라주세요:
    {{
        "word": "단어",
        "meaning": "간단한 한국어 뜻",
        "description": "자세한 설명 (한국어)",
        "wordForms": [
            {{"word": "단어 형태", "pos": "품사 (영어)"}},
            ...
        ],
        "examples": [
            {{"sentence": "영어 예문", "translation": "한국어 번역"}},
            {{"sentence": "영어 예문", "translation": "한국어 번역"}},
            {{"sentence": "영어 예문", "translation": "한국어 번역"}}
        ],
        "relatedWords": ["관련단어1", "관련단어2", "관련단어3"]
    }}
    
    품사는 다음 중 하나를 사용해주세요: noun, verb, adjective, adverb, pronoun, preposition, conjunction, interjection
    
    응답은 반드시 유효한 JSON 형태로만 해주세요. 추가 설명은 넣지 마세요.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates word data in JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        word_data = json.loads(content)
        return word_data
        
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        print(f"받은 응답: {content}")
        raise ValueError("OpenAI 응답을 JSON으로 파싱할 수 없습니다.")
    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        raise ValueError(f"단어 데이터 생성 중 오류: {str(e)}")

def validate_word_data(word_data: Dict) -> bool:
    required_fields = ["word", "meaning", "examples"]
    
    for field in required_fields:
        if field not in word_data:
            print(f"필수 필드 누락: {field}")
            return False
    
    if not isinstance(word_data["examples"], list) or len(word_data["examples"]) == 0:
        print("examples는 비어있지 않은 리스트여야 합니다.")
        return False
    
    for example in word_data["examples"]:
        if not isinstance(example, dict) or "sentence" not in example or "translation" not in example:
            print("각 example은 sentence와 translation을 포함해야 합니다.")
            return False
    
    return True