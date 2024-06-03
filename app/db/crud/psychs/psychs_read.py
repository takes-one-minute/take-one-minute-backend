from sqlalchemy.orm import Session, joinedload
from db.schemas import psychs_schma, user_schema
from db.models import user_model, psych_model
from db.crud.user import user_read
from datetime import datetime, timezone

from typing import List

def get_psych_posts_with_authors(db: Session, page_number: int = 1, limit: int = 10):
    """페이지마다 지정된 수의 게시글을 조회합니다.
    
    Args:
        db (Session): 데이터베이스 세션 객체.
        page_number (int): 현재 페이지 번호, 기본값은 1.
        limit (int): 페이지당 게시글 수, 기본값은 10.
        
    Returns:
        list: 요청된 페이지에 해당하는 게시글 객체 리스트.
    """
    skip = (page_number - 1) * limit  # (현재 페이지 번호 - 1) * 페이지당 게시글 수


    # 게시글과 관련된 작성자 정보를 함께 로드합니다.
    return db.query(psych_model.PsychArticle).options(joinedload(psych_model.PsychArticle.author)).order_by(psych_model.PsychArticle.created_at.desc()).offset(skip).limit(limit).all()


def get_psych_post(db: Session, post_id: int) -> psychs_schma.PsychArticleResponse:
    """특정 게시글을 조회합니다.
    
    Args:
        db (Session): 데이터베이스 세션 객체.
        post_id (int): 조회할 게시글의 ID.
        
    Returns:
        PsychTestPost: 조회된 게시글과 작성자 정보를 포함한 객체.
    """

    post = db.query(psych_model.PsychArticle).filter(psych_model.PsychArticle.id == post_id).first()

    post.try_count += 1
    db.commit()


    if post:
        author_profile = user_read.get_user_profile(db=db, user_id=post.author_id)
        
        return psychs_schma.PsychArticleResponse(
            href=f"/psychs/article/{post.id}",
            id=post.id,
            title=post.title,
            description=post.description,
            type=post.type.value,
            author_id=post.author_id,
            author_nickname=post.author.nickname,
            author_profile_url=author_profile,
            created_at=post.created_at,
            updated_at=post.updated_at,
            thumbnail_url=post.thumbnail_url,
            try_count=post.try_count+1
        )

    return None