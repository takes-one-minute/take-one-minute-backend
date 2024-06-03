from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.schemas import psychs_schma, user_schema
from db.models import user_model, psych_model
from utils import hash
from db.crud.user import user_read
from datetime import datetime, timezone

async def create_article(db: Session, article: psychs_schma.PsychArticleCreate, user_id: int):
    """새로운 검사 글을 생성합니다."""
    # 심리 검사일때의 처리
    if article.type == psychs_schma.PsychType.PSYCH:
        db_article = psych_model.PsychArticle(
            title=article.title,
            description=article.description,
            type=article.type,
            visibility=article.article_visibility,
            thumbnail_url=article.thumbnail_url,
            created_at=datetime.now(timezone.utc),
            author_id=user_id
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        # 일부 공개일 때의 처리
        if article.article_visibility == psychs_schma.PsychVisibility.LIMITED:
            # 비밀번호가 없을 경우 예외 발생
            if article.password is None or article.password == "":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
            db_password = psych_model.PsychArticlePassword(
                password=hash.hash_text(article.password),
                article_id=db_article.id
            )
            db.add(db_password)
        
        # 게시글의 질문들 추가
        if article.questions and len(article.questions) >= 1:
            questions = [
                psych_model.PsychArticleQuestions(
                    title=q.title,
                    description=q.description,
                    score=q.score,
                    article_id=db_article.id
                )
                for q in article.questions
            ]
            db.add_all(questions)

        # 게시글의 결과들 추가
        if article.results and len(article.results) >= 1:
            results = [
                psych_model.PsychArticleResult(
                    title=r.title,
                    description=r.description,
                    score=r.score,
                    article_id=db_article.id
                )
                for r in article.results
            ]
            db.add_all(results)

    # 모든 변경 사항을 한 번에 데이터베이스에 커밋
    db.commit()
    return db_article
