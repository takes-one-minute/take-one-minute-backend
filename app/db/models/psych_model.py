from db.session import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BigInteger, SmallInteger, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from datetime import datetime, timezone

class PsychArticle(Base):
    __tablename__ = "psych_articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    thumbnail_url = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime)
    try_count = Column(Integer, nullable=False, default=0) # 이 테스트를 시도해본 수(조회수)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    questions = relationship("PsychArticleQuestions", back_populates="post")
    results = relationship("PsychArticleResult", back_populates="post")

class PsychArticleQuestions(Base):
    __tablename__ = "psych_article_questions"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text) 
    score = Column(Integer, nullable=False, default=0)

    post_id = Column(Integer, ForeignKey('psych_articles.id'))
    post = relationship("PsychArticle", back_populates="questions")

class PsychArticleResult(Base):
    __tablename__ = "psych_article_results"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    score = Column(Integer, nullable=False, default=0)

    post_id = Column(Integer, ForeignKey('psych_articles.id'))
    post = relationship("PsychArticle", back_populates="results")

