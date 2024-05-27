from sqlalchemy.orm import Session
from app.db.schemas.user_schema import *
from app.db.models import user_model
from app.utils import hash
from app.db.crud.user import user_read
from datetime import datetime, timezone

async def create_user(db: Session, user: UserCreate):
    """새로운 사용자를 생성합니다."""
    db_user = user_model.User(
        username=user.username,
        email=user.email,
        nickname=user.nickname,
        hashed_password=hash.hash_text(user.password),
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_jwt(db: Session, user_id: int, access_token: str, refresh_token: str, public_ip: str):
    """새로운 JWT 토큰을 생성합니다."""
    db_token = user_model.JwtToken(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        public_ip=public_ip
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token