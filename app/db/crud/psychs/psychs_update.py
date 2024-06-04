from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.schemas import psychs_schma, user_schema
from db.models import user_model, psych_model
from utils import hash
from db.crud.user import user_read
from datetime import datetime, timezone

import traceback


async def update_article(db: Session, article_id: int, psychs: psychs_schma.PsychArticleUpdate):
    """
        articleをアップデートする。
    """

    try:
        db_post = db.query(psych_model.PsychArticle).filter(psych_model.PsychArticle.id == article_id).first()

        if not db_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

        if len(psychs.title) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title Too Short")

        db_post.title = psychs.title
        db_post.description = psychs.description
        db_post.visibility = psychs.article_visibility
        db_post.thumbnail_url = psychs.thumbnail_url
        db_post.updated_at = datetime.now(timezone.utc)

        db.commit()

    except SQLAlchemyError as e:
        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")