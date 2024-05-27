from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PsychArticleBase(BaseModel):
    title: str
    description: str

class PsychArticleBaseScore(PsychArticleBase):
    score: int

class PsychArticleCreate(PsychArticleBase):
    thumbnail_url: Optional[str] = None
    questions: List[PsychArticleBaseScore] = None
    results: List[PsychArticleBaseScore] = None

class PsychArticleResponse(PsychArticleBase):
    id: int
    author_id: int
    author_nickname: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    try_count: int

class PsychArticlesResponse(BaseModel):
    posts: List[PsychArticleResponse] = Field(default_factory=list)