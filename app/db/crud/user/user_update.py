from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.db.crud.user import user_read

async def update_user_for_login(db: Session, db_user, public_ip: str, last_login: datetime = datetime.now(timezone.utc)):
    """사용자의 로그인 정보를 업데이트합니다."""
    db_user.last_login = last_login
    db_user.public_ip = public_ip
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_user_last_login(db: Session, user_id: int):
    """사용자의 마지막 로그인 시간을 업데이트합니다."""
    db_user = user_read.get_user_by_id(db, user_id)
    db_user.last_login = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_user_public_ip(db: Session, user_id: int):
    """사용자의 마지막 로그인 시간을 업데이트합니다."""
    db_user = user_read.get_user_by_id(db, user_id)
    db_user.last_login = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user