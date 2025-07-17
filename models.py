# models.py - 데이터 모델
from pydantic import BaseModel
from typing import List

class WordForm(BaseModel):
    word: str
    pos: str

class Example(BaseModel):
    sentence: str
    translation: str

class WordEntry(BaseModel):
    id: str
    word: str
    shortMeaning: str
    detailedMeaning: str
    wordForms: List[WordForm]
    examples: List[Example]
    relatedWords: List[str]

class WordEntryCreate(BaseModel):
    word: str
    shortMeaning: str
    detailedMeaning: str
    wordForms: List[WordForm] = []
    examples: List[Example] = []
    relatedWords: List[str] = []