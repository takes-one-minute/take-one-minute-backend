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
        user_id = await jwt.get_user_id_from_token(token=access_token)
        db_user = user_read.find_user_by_userid(db, user_id)

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Create a new post
        new_article_id = await psychs_create.create_article(db, article, user_id)

        return {
            "detail": new_article_id
        }

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
                href=f"/psychs/{article.id}",
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
                view_count=article.view_count,
                article_visibility=article.visibility
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


# 특성 게시글 수정
@router.patch("/article/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_article(
    id: int, 
    psych: psychs_schma.PsychArticleUpdate, 
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        user_id = await jwt.get_user_id_from_token(token=access_token)
        psychs_owner_id = psychs_read.get_psych_owner(db=db, article_id=id)

        if user_id != psychs_owner_id:
            if not await jwt.token_has_permission(db=db, token=access_token):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        await psychs_update.update_article(db=db, article_id=id, psychs=psych)

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
@router.get("/article/{id}", response_model=psychs_schma.PsychArticleResponse, status_code=status.HTTP_200_OK)
async def read_article(id: int, db: Session = Depends(get_db)):
    try:
        # Get the post
        db_post = psychs_read.get_psych_post(db, id)
        if not db_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return db_post

        return return_data

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
@router.get("/psych/{id}", response_model=psychs_schma.PsychArticleQuestions, status_code=status.HTTP_200_OK)
async def read_psych_test(id: int, db: Session = Depends(get_db)):
    try:
        # Get the questions
        db_questions = psychs_read.get_psych_questions_and_answer(db=db, article_id=id)
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


@router.get("/psych/{id}/statistics", response_model=psychs_schma.PsychArticleQuestionStatistics, status_code=status.HTTP_200_OK)
async def get_psych_question_statistics(
    id: int,
    access_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    user_id = await jwt.get_user_id_from_token(token=access_token)
    psychs_owner_id = psychs_read.get_psych_owner(db=db, article_id=id)

    if user_id != psychs_owner_id:
        if not await jwt.token_has_permission(db=db, token=access_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return psychs_read.get_psych_question_statistics(db=db, article_id=id)


@router.post("/psych/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_psych_to_article(
    id: int, 
    psychs: psychs_schma.PsychArticleQuestions,
    access_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    user_id = await jwt.get_user_id_from_token(token=access_token)
    psychs_owner_id = psychs_read.get_psych_owner(db=db, article_id=id)

    if user_id != psychs_owner_id:
        if not await jwt.token_has_permission(db=db, token=access_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    await add_psych_to_article(db=db, article_id=id, psychs=psychs.questions)