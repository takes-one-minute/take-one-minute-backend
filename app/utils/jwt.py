from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from core.config import get_settings
from fastapi import HTTPException

async def create_token(subject: str , user_id: int, expires_delta: timedelta = None):
    current_utc_time = datetime.now(timezone.utc)
    expire = current_utc_time + expires_delta if expires_delta else current_utc_time + timedelta(minutes=1)
    payload = { "sub": subject, "user_id": user_id, "exp": expire }

    settings = get_settings()
    encoded_jwt = jwt.encode(payload, settings.access_secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def create_access_token(subject: str, user_id: int):
    encoded_jwt = await create_token(subject, user_id, timedelta(hours=4))
    return encoded_jwt

async def create_refresh_token(subject: str, user_id: int):
    encoded_jwt = await create_token(subject, user_id, timedelta(days=7))
    return encoded_jwt

async def verify_token(token: str):
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