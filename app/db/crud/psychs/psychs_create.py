from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.schemas import psychs_schma, user_schema
from db.models import user_model, psych_model
from utils import hash
from db.crud.user import user_read
from datetime import datetime, timezone

import traceback

async def create_article(db: Session, article: psychs_schma.PsychArticleCreate, user_id: int):
    """새로운 검사 글을 생성합니다."""

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


    # 심리 검사일때의 처리
    # if article.type == psychs_schma.PsychType.PSYCH:
    #     # 게시글의 질문들 추가
    #     if article.questions and len(article.questions) >= 1:
    #         questions = [
    #             psych_model.PsychArticleQuestions(
    #                 title=q.title,
    #                 description=q.description,
    #                 score=q.score,
    #                 article_id=db_article.id
    #             )
    #             for q in article.questions
    #         ]
    #         db.add_all(questions)

    #     # 게시글의 결과들 추가
    #     if article.results and len(article.results) >= 1:
    #         results = [
    #             psych_model.PsychArticleResult(
    #                 title=r.title,
    #                 description=r.description,
    #                 score=r.score,
    #                 article_id=db_article.id
    #             )
    #             for r in article.results
    #         ]
    #         db.add_all(results)

    # 모든 변경 사항을 한 번에 데이터베이스에 커밋
    db.commit()

    return db_article.id


async def add_psych_to_article(db: Session, article_id: int, psychs: psychs_schma.PsychArticleQuestions):
    """
        검사를 테스트에 추가합니다.
    """

    try:
        for psych in psychs:
            question = psych_model.PsychArticleQuestions(
                article_id=article_id,
                question=psych.title,
                description=psych.description,
                score=psych.score or 0,
            )

            db.add(question)
            db.commit()

            question_id = question.id

            if psych.attachment:
                attachment = psych_model.PsychArticleQuestionAttachment()

                if psych.attachment.image:
                    attachment.image = psych.attachment.image

                if psych.attachment.video:
                    attachment.video = psych.attachment.video

                if psych.attachment.audio:
                    attachment.audio = psych.attachment.audio

                db.add(attachment)
                db.commit()

    except SQLAlchemyError as e:
        err_msg = traceback.format_exc()
        print(err_msg)

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")