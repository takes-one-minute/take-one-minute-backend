from sqlalchemy.orm import Session
from app.db.schemas import psychs_schma, user_schema
from app.db.models import user_model, psych_model
from app.utils import hash
from app.db.crud.user import user_read
from datetime import datetime, timezone

async def create_post(db: Session, post: psychs_schma.PsychArticleCreate, user_id: int):
    """새로운 게시글을 생성합니다."""
    # 게시글 객체 생성
    db_post = psych_model.PsychArticle(
        author_id=user_id,
        title=post.title,
        description=post.description,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # 게시글의 질문들 추가
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

    # 필요한 경우 여기에서 객체를 refresh 할 수 있습니다
    db.refresh(db_post)
    for question in questions:
        db.refresh(question)
    for result in results:
        db.refresh(result)

    return db_post
