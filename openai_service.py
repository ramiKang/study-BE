import os
import json
from openai import OpenAI
from typing import List, Dict

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_word_data(word: str) -> Dict:
    """
    OpenAI API를 사용하여 영단어 정보를 생성합니다.
    
    Args:
        word (str): 영단어
        
    Returns:
        Dict: 단어 정보 객체
    """
    
    prompt = f"""Generate a JSON object for the given word, following this schema:

{{
  "word": "",
  "meaning": "짧은 한국어 의미 (1-2단어)",
  "description": "Provide a clear, detailed English explanation considering the computer science and research context.(100자 이내)",
  "wordForms": [
    {{"word": "", "pos": "noun|verb|adjective|adverb|pronoun|preposition|conjunction|interjection"}}
  ],
  "examples": [
    {{"sentence": "English sentence from a research context", "translation": "한국어 번역"}}
  ],
  "relatedWords": ["", "", ""]
}}

Rules:
- Ensure JSON is valid.
- meaning: short Korean meaning (1-3 words).
- description: English explanation, NOT Korean, adapted to computer science context.
- wordForms: common variations with POS chosen from: noun, verb, adjective, adverb, pronoun, preposition, conjunction, interjection.
- examples: 1 to 1 examples, in natural academic English, each with a Korean translation.
- relatedWords: 2 to 3 semantically related terms in English.
- Do NOT add extra text, explanations, or comments outside the JSON.

Word: {word}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert in computer science and technical English. Your task is to provide accurate definitions and examples for English terms commonly used in computer science research. Return the result strictly in JSON format according to the provided schema."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        content = response.choices[0].message.content.strip()
        
        # markdown 코드 블록 제거
        if content.startswith("```json"):
            content = content[7:]  # ```json 제거
        elif content.startswith("```"):
            content = content[3:]   # ``` 제거
        
        if content.endswith("```"):
            content = content[:-3]  # 끝의 ``` 제거
        
        content = content.strip()
        
        # JSON 파싱
        try:
            word_data = json.loads(content)
            return word_data
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            print(f"응답 내용: {content}")
            raise ValueError(f"OpenAI 응답을 JSON으로 파싱할 수 없습니다: {e}")
            
    except Exception as e:
        print(f"OpenAI API 호출 오류: {e}")
        raise ValueError(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")


def validate_word_data(word_data: Dict) -> bool:
    """
    생성된 단어 데이터가 올바른 형식인지 검증합니다.
    
    Args:
        word_data (Dict): 검증할 단어 데이터
        
    Returns:
        bool: 유효한 경우 True, 그렇지 않으면 False
    """
    required_fields = ["word", "meaning", "examples"]
    
    # 필수 필드 확인
    for field in required_fields:
        if field not in word_data:
            return False
    
    # 품사 유효성 검사
    valid_pos = ["noun", "verb", "adjective", "adverb", "pronoun", "preposition", "conjunction", "interjection"]
    
    if word_data.get("wordForms"):
        for form in word_data["wordForms"]:
            if form.get("pos") and form["pos"] not in valid_pos:
                return False
    
    # examples 필드 검증
    if not isinstance(word_data["examples"], list) or len(word_data["examples"]) == 0:
        return False
    
    for example in word_data["examples"]:
        if not isinstance(example, dict) or "sentence" not in example or "translation" not in example:
            return False
    
    return True