from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    nickname: str


class UserCreate(UserBase):
    password: str
    public_ip: Optional[str] = None



class User(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class JwtToken(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True