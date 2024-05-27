from sqlalchemy.orm import Session
from db.schemas import user_schema
from db.models import user_model
from db.crud.user import user_read
from sqlalchemy import and_
from fastapi import HTTPException
