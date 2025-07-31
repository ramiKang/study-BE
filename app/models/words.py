from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PosType(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"

class WordForm(BaseModel):
    word: str
    pos: PosType

class Example(BaseModel):
    sentence: str
    translation: str

class WordEntry(BaseModel):
    id: str
    word: str
    meaning: str
    description: Optional[str] = None
    wordForms: Optional[List[WordForm]] = None
    examples: List[Example]
    relatedWords: Optional[List[str]] = None

class WordEntryCreate(BaseModel):
    word: str
    meaning: str
    description: Optional[str] = None
    wordForms: Optional[List[WordForm]] = None
    examples: List[Example] = Field(default_factory=list)
    relatedWords: Optional[List[str]] = None