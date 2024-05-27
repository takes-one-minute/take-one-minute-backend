from app.db.session import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, BigInteger, SmallInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nickname = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_login = Column(DateTime)

    posts = relationship("PsychArticle", back_populates="author")
    tokens = relationship("JwtToken", back_populates="user")

class JwtToken(Base):
    __tablename__ = "jwt_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String(255), nullable=False, index=True)
    refresh_token = Column(String(255), nullable=False)
    public_ip = Column(String(50), nullable=False)

    user = relationship("User", back_populates="tokens")