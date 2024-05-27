from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    username: str
    email: str
    nickname: str

class UserCreate(UserBase):
    password: str
    public_ip: str

class UserLogin(BaseModel):
    account: str
    password: str
    public_ip: str

class User(UserBase):
    id: int
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime]

    class Config:
        from_attributes = True

class JwtToken(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True