from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PsychType(Enum):
    PSYCH = "psych"
    QUIZ = "quiz"
    TOURNAMENT = "tournament"


class PsychArticleBase(BaseModel):
    title: str
    description: str
    type: PsychType

class PsychArticleBaseScore(BaseModel):
    title: str
    description: str
    score: int


class PsychArticleCreate(PsychArticleBase):
    thumbnail_url: Optional[str] = None
    questions: Optional[List[PsychArticleBaseScore]] = None
    results: Optional[List[PsychArticleBaseScore]] = None


class PsychArticleResponse(PsychArticleBase):
    href: str
    id: int
    author_id: int
    author_profile_url: Optional[str] = None
    author_nickname: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    thumbnail_url: Optional[str] = None
    try_count: int


class PsychArticlesResponse(BaseModel):
    posts: List[PsychArticleResponse] = Field(default_factory=list)