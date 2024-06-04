from sqlalchemy.orm import Session
from db.models import user_model
from db.schemas import user_schema
from sqlalchemy import or_, and_, union_all

from utils.jwt import Permission

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
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

    if user:    
        profile = get_user_profile(db=db, user_id=user.id)

        return user_schema.User(
            id=user.id,
            username=user.username,
            email=user.email,
            nickname=user.nickname,
            created_at=user.created_at,
            last_login=user.last_login,
            profile_url=profile
        )

    return None


def get_user_profile(db: Session, user_id: int):
    profile = db.query(user_model.UserProfile).filter(user_model.UserProfile.user_id == user_id).first()

    if profile:
        return profile.profile_url

    return None


def get_user_name(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

    if user:
        return user.nickname

    return None


def get_user_permission(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

    if user:
        permissions = ["-"]

        result = [
            Permission(perm)
            for perm in permissions
        ] 

        return result

    return None