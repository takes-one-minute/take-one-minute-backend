from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.session import get_db
from db.schemas import user_schema, psychs_schma
from db.crud.user import user_create, user_read, user_update, user_delete
from db.crud.psychs import psychs_create, psychs_read, psychs_update, psychs_delete

from utils import utils, jwt, hash

import traceback

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.post("/article", status_code=status.HTTP_201_CREATED)
async def create_article(article: psychs_schma.PsychArticleCreate, access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
        await psychs_create.create_article(db, article, user_id)

        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Post created successfully")

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

@router.get("/articles", response_model=psychs_schma.PsychArticlesResponse, status_code=status.HTTP_200_OK)
async def read_articles(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        # Get the post list
        db_articles = psychs_read.get_psych_posts_with_authors(db, page, limit)
        if not db_articles:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        articles_list = []

        for article in db_articles:
            author_profile = user_read.get_user_profile(db=db, user_id=article.author_id)
            articles_list.append(psychs_schma.PsychArticleResponse(
                href=f"/psychs/article/{article.id}",
                id=article.id,
                title=article.title,
                type=article.type.value,
                description=article.description,
                author_id=article.author_id,
                author_profile_url=author_profile,
                author_nickname=article.author.nickname if article.author else 'Unknown',
                thumbnail_url=article.thumbnail_url,
                created_at=article.created_at.isoformat() if article.created_at else None,
                updated_at=article.updated_at.isoformat() if article.updated_at else None,
                view_count=article.view_count
            ))

        return psychs_schma.PsychArticlesResponse(posts=articles_list)

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

# 특정 게시글 조회 (단일 게시글 조회)
@router.get("/article", response_model=psychs_schma.PsychArticleResponse, status_code=status.HTTP_200_OK)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    try:
        # Get the post
        db_post = psychs_read.get_psych_post(db, article_id)
        if not db_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return db_post

        return return_data

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

# 테스트 진행(질문들 가져오기)
@router.get("/psych", response_model=psychs_schma.PsychArticleQuestions, status_code=status.HTTP_200_OK)
async def read_psych_test(article_id: int, db: Session = Depends(get_db)):
    try:
        # Get the questions
        db_questions = psychs_read.get_psych_questions_and_answer(db, article_id)
        if not db_questions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questions not found")
        
        return db_questions

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