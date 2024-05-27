from sqlalchemy.orm import Session
from db.models import user_model
from sqlalchemy import or_, and_

def find_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def find_user_by_username(db: Session, username: str):
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def find_user_by_nickname(db: Session, nickname: str):
    return db.query(user_model.User).filter(user_model.User.nickname == nickname).first()

def find_user_for_login(db: Session, account: str):
    return db.query(user_model.User).filter(or_(user_model.User.email == account, user_model.User.username == account)).first()

def find_user_for_register(db: Session, email: str, username: str, nickname: str):
    return db.query(user_model.User).filter(or_(user_model.User.email == email, user_model.User.username == username, user_model.User.nickname == nickname)).first()

def find_user_by_userid(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()
