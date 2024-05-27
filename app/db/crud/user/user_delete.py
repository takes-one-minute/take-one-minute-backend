from sqlalchemy.orm import Session
from app.db.schemas import user_schema
from app.db.models import user_model
from app.db.crud.user import user_read
from sqlalchemy import and_
from fastapi import HTTPException
