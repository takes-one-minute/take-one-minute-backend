from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from core.config import get_settings
from fastapi import HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from db.session import get_db
from db.crud.user import user_read

from enum import Enum

class Permission(Enum):
    ADMIN = "*"
    MODERATOR = "mod"
    USER = "-"

async def create_token(subject: str , user_id: int, expires_delta: timedelta = None):
    current_utc_time = datetime.now(timezone.utc)
    expire = current_utc_time + expires_delta if expires_delta else current_utc_time + timedelta(minutes=1)
    payload = { "sub": subject, "uid": user_id, "perm": ['-'], "iat": current_utc_time, "exp": expire }

    settings = get_settings()
    encoded_jwt = jwt.encode(payload, settings.access_secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def create_access_token(subject: str, user_id: int):
    encoded_jwt = await create_token(subject, user_id, timedelta(hours=4))
    return encoded_jwt

async def create_refresh_token(subject: str, user_id: int):
    encoded_jwt = await create_token(subject, user_id, timedelta(days=7))
    return encoded_jwt

async def is_token_vaildate(token: str):
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token,
            settings.access_secret_key,
            algorithms=[settings.algorithm]
        )
        exp = payload.get('exp')

        if exp is None or datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_token_body(token: str):
    if await is_token_vaildate(token):
        settings = get_settings()
        try:
            payload = jwt.decode(
                token,
                settings.access_secret_key,
                algorithms=[settings.algorithm]
            )
            
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


async def get_user_id_from_token(token: str):
    if await is_token_vaildate(token):
        settings = get_settings()
        try:
            payload = jwt.decode(
                token,
                settings.access_secret_key,
                algorithms=[settings.algorithm]
            )
            
            return int(payload.get('uid'))
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


async def token_has_permission(db: Session, token: str, perm: List[Permission] = []):
    """
        토큰의 sub에서 사용자 ID를 추출 후 DB에서 가져와 권한을 확인합니다.
        :param token: 검사 할 
        :param perm: 체크할 권한의 배열입니다.

        기본적으로 Administrator (*)와 Moderator (mod)는 권한 검사에서 통과됩니다. 

        :return: **boolean 값**
        ###
    """
    user_id = await get_user_id_from_token(token=token)

    permission = await user_read.get_user_permission(db=db, user_id=user_id)

    if Permission.ADMIN in permission or Permission.MODERATOR in permission:
        return True

    else:
        # 권한 체크
        for required_perm in permi:
            if required_perm in permission:
                return True # 권한이 포함되어 있으면 그대로 리턴
        # 여기까지 왔다면 권한이 없음
        return False
