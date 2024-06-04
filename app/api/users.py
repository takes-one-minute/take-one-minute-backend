from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.session import get_db
from db.schemas import user_schema
from db.crud.user import user_create, user_read, user_update, user_delete

from utils import utils, jwt, hash

import traceback

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.post("/register", response_model=user_schema.JwtToken, status_code=status.HTTP_201_CREATED)
async def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the email is valid
        if not utils.is_valid_email(user.email):
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Check if the email or username or nickname is already registered
        if user_read.find_user_for_register(db, user.email, user.username, user.nickname):
            raise HTTPException(status_code=400, detail="Email or username or nickname already registered")

        # Create a new user
        db_user = await user_create.create_user(db, user)
        
        # Create JWT tokens
        access_token = await jwt.create_access_token("access", db_user.id)
        refresh_token = await jwt.create_refresh_token("refresh", db_user.id)
        await user_create.create_jwt(db, db_user.id, access_token, refresh_token, user.public_ip)

        return user_schema.JwtToken(access_token=access_token, refresh_token=refresh_token)

    except HTTPException as http_ex:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise http_ex

    except SQLAlchemyError as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()

@router.post("/login", response_model=user_schema.JwtToken, status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # Check if the email is valid
        db_user = user_read.find_user_for_login(db, form_data.username)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Check if the password is valid
        if not hash.verify_hashed_text(form_data.password, db_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        
        # Update the last public IP and last login time
        await user_update.update_user_for_login(db, db_user, "0.0.0.0")
        
        # Create JWT tokens
        access_token = await jwt.create_access_token("access", db_user.id)
        refresh_token = await jwt.create_refresh_token("refresh", db_user.id)
        await user_create.create_jwt(db, db_user.id, access_token, refresh_token, "0.0.0.0")
        return user_schema.JwtToken(access_token=access_token, refresh_token=refresh_token)
    
    except HTTPException as http_ex:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise http_ex

    except SQLAlchemyError as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()

@router.post("/refresh", response_model=user_schema.JwtToken, status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Verify the refresh token
        user_id = await jwt.get_user_id_from_token(token=token)
        
        access_token = await jwt.create_access_token("access", user_id)
        return user_schema.JwtToken(access_token=access_token, refresh_token=refresh_token)
    
    except HTTPException as http_ex:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise http_ex

    except SQLAlchemyError as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()

@router.get("/me", response_model=user_schema.User, status_code=status.HTTP_200_OK)
async def read_user_me(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Verify the access token
        user_id = await jwt.get_user_id_from_token(token=access_token)
        db_user = user_read.find_user_by_userid(db, user_id)
        
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return db_user
    
    except HTTPException as http_ex:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise http_ex

    except SQLAlchemyError as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        db.rollback()

        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()