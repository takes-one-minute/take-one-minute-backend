from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PsychType(Enum):
    PSYCH = "psych"
    QUIZ = "quiz"
    TOURNAMENT = "tournament"

class PsychVisibility(Enum):
    PUBLIC = "public" # 공개
    PRIVATE = "private" # 비공개
    LIMITED = "limited" # 일부공개

class PsychArticleBase(BaseModel):
    title: str
    description: str
    type: PsychType

class PsychArticleAnswer(BaseModel):
    answer: str
    score: int

class PsychArticleAnswerStatistics(PsychArticleAnswer):
    answer: str
    score: int
    count: int

class PsychArticleQuestionAttachment(BaseModel):
    image: Optional[str] = None
    video: Optional[str] = None
    audio: Optional[str] = None

class PsychArticleQuestion(BaseModel):
    index: int
    question: str
    description: Optional[str]
    attachment: Optional[PsychArticleQuestionAttachment] = None
    answers: List[PsychArticleAnswer]

class PsychArticleQuestionStatistic(BaseModel):
    index: int
    question: str
    description: Optional[str]
    attachment: Optional[PsychArticleQuestionAttachment] = None
    answers: List[PsychArticleAnswerStatistics]

class PsychArticleQuestions(BaseModel):
    questions: List[PsychArticleQuestion] = Field(default_factory=list)

class PsychArticleQuestionStatistics(BaseModel):
    questions: List[PsychArticleQuestionStatistic] = Field(default_factory=list)

class PsychArticleCreate(PsychArticleBase):
    article_visibility : PsychVisibility
    password : Optional[str] = None
    thumbnail_url: Optional[str] = None
    # questions: Optional[List[PsychArticleQuestion]] = None


class PsychArticleUpdate(PsychArticleCreate):
    pass


class PsychArticleResponse(PsychArticleBase):
    href: str
    id: int
    author_id: int
    author_profile_url: Optional[str] = None
    author_nickname: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    thumbnail_url: Optional[str] = None
    article_visibility: PsychVisibility
    view_count: int

class PsychArticlesResponse(BaseModel):
    posts: List[PsychArticleResponse] = Field(default_factory=list)
