from db.session import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BigInteger, SmallInteger, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from db.schemas import psychs_schma
# from sqlalchemy.dialects.postgresql import ENUM

from datetime import datetime, timezone

class PsychArticle(Base):
    __tablename__ = "psych_articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    type = Column(Enum(psychs_schma.PsychType), nullable=False)
    visibility = Column(Enum(psychs_schma.PsychVisibility), nullable=False, default=psychs_schma.PsychVisibility.PUBLIC)

    thumbnail_url = Column(String(255))
    
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime)
    view_count = Column(Integer, nullable=False, default=0)

    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship("User", back_populates="articles")
    questions = relationship("PsychArticleQuestions", back_populates="article")
    results = relationship("PsychArticleResult", back_populates="article")
    password = relationship("PsychArticlePassword", back_populates="article", uselist=False) # 일대일 관계 설정


class PsychArticleQuestions(Base):
    __tablename__ = "psych_article_questions"

    id = Column(Integer, primary_key=True)
    question = Column(String(255), nullable=False)
    description = Column(Text)

    article_id = Column(Integer, ForeignKey('psych_articles.id'))

    article = relationship("PsychArticle", back_populates="questions")
    answers = relationship("PsychArticleAnswer", back_populates="question", cascade="all, delete-orphan") # cascade="all, delete-orphan" = 부모가 삭제되면 자식도 삭제됨(일대다관계 설정)
    attachments = relationship("PsychArticleQuestionAttachment", back_populates="question", cascade="all, delete-orphan")


class PsychArticleQuestionAttachment(Base):
    __tablename__ = "psych_article_attachment"

    id = Column(Integer, primary_key=True)

    image = Column(String(255))
    video = Column(String(255))
    audio = Column(String(255))

    question_id = Column(Integer, ForeignKey('psych_article_questions.id'))

    question = relationship("PsychArticleQuestions", back_populates="attachments")


class PsychArticleAnswer(Base):
    __tablename__ = "psych_article_answers"
    
    id = Column(Integer, primary_key=True)
    answer = Column(Text, nullable=False)
    score = Column(Integer, nullable=False, default=0)

    article_id = Column(Integer, ForeignKey('psych_articles.id'))
    question_id = Column(Integer, ForeignKey('psych_article_questions.id'))
    
    question = relationship("PsychArticleQuestions", back_populates="answers")

class PsychArticleResult(Base):
    __tablename__ = "psych_article_results"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)

    article_id = Column(Integer, ForeignKey('psych_articles.id'))

    article = relationship("PsychArticle", back_populates="results")



class PsychArticlePassword(Base):
    __tablename__ = "psych_article_passwords"

    id = Column(Integer, primary_key=True)
    password = Column(String(255), nullable=False)

    article_id = Column(Integer, ForeignKey('psych_articles.id'))

    article = relationship("PsychArticle", back_populates="password")