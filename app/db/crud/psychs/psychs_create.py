from sqlalchemy.orm import Session
from db.schemas import psychs_schma, user_schema
from db.models import user_model, psych_model
from utils import hash
from db.crud.user import user_read
from datetime import datetime, timezone

async def create_post(db: Session, post: psychs_schma.PsychArticleCreate, user_id: int):
    """새로운 검사를 생성합니다."""

    # 게시글 객체 생성
    db_post = psych_model.PsychArticle(
        title=post.title,
        description=post.description,

        type=post.type,

        thumbnail_url=post.thumbnail_url,
        created_at=datetime.now(timezone.utc),
        author_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # 심리 검사일때의 처리
    if post.type == psychs_schma.PsychType.PSYCH:
        # 게시글의 질문들 추가
        if post.questions and len(post.questions) >= 1:
            questions = [
                psych_model.PsychArticleQuestions(
                    title=q.title,
                    description=q.description,
                    score=q.score,
                    post_id=db_post.id
                )
                for q in post.questions
            ]
            db.add_all(questions)

        # 게시글의 결과들 추가
        if post.results and len(post.results) >= 1:
            results = [
                psych_model.PsychArticleResult(
                    title=r.title,
                    description=r.description,
                    score=r.score,
                    post_id=db_post.id
                )
                for r in post.results
            ]
            db.add_all(results)

    # 모든 변경 사항을 한 번에 데이터베이스에 커밋
    db.commit()
    return db_post
