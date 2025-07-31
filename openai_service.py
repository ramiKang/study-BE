import os
import json
from openai import OpenAI
from typing import List, Dict

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_word_data(word: str) -> Dict:
    prompt = f"""Generate a JSON object for the given word, following this schema:

{{
  "word": "",
  "meaning": "짧은 한국어 의미를 1개 이상, 최대 5개까지 쉼표로 구분하여 작성 (예: 처리하다, 실행하다, 작동하다)",
  "description": "Provide a detailed English explanation of up to 150 characters, focusing on its meaning in computer science and research contexts.",
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
- meaning: include up to 5 short Korean meanings, separated by commas.
- description: clear, detailed English explanation (max 150 characters), focusing on computer science usage.
- wordForms: include only derived forms of the word (exclude the original word), each with a POS from the list.
- examples: provide 1 academic English sentence with Korean translation.
- relatedWords: provide 2 or 3 semantically related English words.
- Do NOT add any extra text or comments outside the JSON.

Word: {word}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert in computer science, cybersecurity, and technical English. Your task is to provide accurate definitions and examples for English terms commonly used in computer science and security research. Return the result strictly in JSON format according to the provided schema."},
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