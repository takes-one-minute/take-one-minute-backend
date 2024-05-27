from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.session import get_db
from db.schemas import user_schema, psychs_schma
from db.crud.user import user_create, user_read, user_update, user_delete
from db.crud.psychs import psychs_create, psychs_read, psychs_update, psychs_delete

from utils import utils, jwt, hash

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.post("/article", response_model=psychs_schma.PsychArticleCreate, status_code=status.HTTP_201_CREATED)
async def create_post(post: psychs_schma.PsychArticleCreate, access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Verify the access token
        payload = await jwt.verify_token(access_token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # Get the user information
        user_id = payload.get("user_id")
        db_user = user_read.find_user_by_userid(db, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create a new post
        db_post = await psychs_create.create_post(db, post, user_id)
        return_data = psychs_schma.PsychArticleCreate(
            id=db_post.id,
            title=db_post.title,
            description=db_post.description,
            author_id=db_post.author_id,
            created_at=db_post.created_at
        )
        return return_data

    except HTTPException as http_ex:
        db.rollback()
        print(http_ex)
        raise http_ex

    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()

@router.get("/articles", response_model=psychs_schma.PsychArticlesResponse, status_code=status.HTTP_200_OK)
async def read_posts(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        # Get the post list
        db_posts = psychs_read.get_psych_posts_with_authors(db, page, limit)
        if not db_posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        post_list = [
            psychs_schma.PsychArticleResponse(
                id=post.id,
                title=post.title,
                description=post.description,
                author_id=post.author_id,
                author_nickname=post.author.nickname if post.author else 'Unknown',
                created_at=post.created_at.isoformat() if post.created_at else None,
                updated_at=post.updated_at.isoformat() if post.updated_at else None,
                try_count=post.try_count
            )
            for post in db_posts
        ]
        return_data = psychs_schma.PsychArticlesResponse(posts=post_list)

        return return_data

    except HTTPException as http_ex:
        print(http_ex)
        raise http_ex

    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()

# 특정 게시글 조회 (단일 게시글 조회)
@router.get("/article", response_model=psychs_schma.PsychArticleResponse, status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    try:
        # Get the post
        db_post = psychs_read.get_psych_post(db, post_id)
        if not db_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        # Update the try count (View count)
        db_post.try_count += 1
        db.commit()
        db.refresh(db_post) 

        return_data = psychs_schma.PsychArticleResponse(
            id=db_post.id,
            title=db_post.title,
            description=db_post.description,
            author_id=db_post.author_id,
            author_nickname=db_post.author.nickname if db_post.author else 'Unknown',  # 조인된 사용자 정보 사용
            created_at=db_post.created_at,
            updated_at=db_post.updated_at,
            try_count=db_post.try_count
        )

        return return_data

    except HTTPException as http_ex:
        db.rollback()
        print(http_ex)
        raise http_ex

    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    finally:
        db.close()