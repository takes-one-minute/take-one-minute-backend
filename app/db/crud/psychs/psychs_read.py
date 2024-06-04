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


def get_psych_post(db: Session, article_id: int) -> psychs_schma.PsychArticleResponse:
    """특정 게시글을 조회합니다.
    
    Args:
        db (Session): 데이터베이스 세션 객체.
        post_id (int): 조회할 게시글의 ID.
        
    Returns:
        PsychTestPost: 조회된 게시글과 작성자 정보를 포함한 객체.
    """

    db_article = db.query(psych_model.PsychArticle).filter(psych_model.PsychArticle.id == article_id).first()

    # 조회수 업데이트
    db_article.view_count += 1
    db.commit()

    if db_article:
        author_profile = user_read.get_user_profile(db=db, user_id=db_article.author_id)
        
        return psychs_schma.PsychArticleResponse(
            href=f"/psychs/{db_article.id}",
            id=db_article.id,
            title=db_article.title,
            description=db_article.description,
            type=db_article.type.value,
            author_id=db_article.author_id,
            author_nickname=db_article.author.nickname,
            author_profile_url=author_profile,
            created_at=db_article.created_at,
            updated_at=db_article.updated_at,
            thumbnail_url=db_article.thumbnail_url,
            view_count=db_article.view_count+1,
            article_visibility=db_article.visibility
        )

    return None

def get_psych_questions_and_answer(db: Session, article_id: int) -> psychs_schma.PsychArticleResponse:
    """특정 게시글의 질문과 답변을 조회합니다.
    
    :param db: 데이터베이스 세션 객체.
    :param article_id: 조회할 게시글의 ID.
    ###
    :return: PsychTestPost: 조회된 게시글과 작성자 정보를 포함한 객체.
    ###
    """

    db_article_questions = db.query(psych_model.PsychArticleQuestions).filter(psych_model.PsychArticleQuestions.article_id == article_id).all()

    questions_list = []

    if db_article_questions:
        for index, db_article_question in enumerate(db_article_questions):

            db_article_answers = db.query(psych_model.PsychArticleAnswer).filter(psych_model.PsychArticleAnswer.question_id == db_article_question.id).all()
            question_attachment = db.query(psych_model.PsychArticleQuestionAttachment).filter(psych_model.PsychArticleQuestionAttachment.question_id == db_article_question.id).first()

            questions_list.append(psychs_schma.PsychArticleQuestion(
                index=index,
                question=db_article_question.question,
                description=db_article_question.description,
                attachment=psychs_schma.PsychArticleQuestionAttachment(
                    image=question_attachment.image,
                    video=question_attachment.video,
                    audio=question_attachment.audio
                ) if question_attachment else None,
                answers=[psychs_schma.PsychArticleAnswer(
                    answer=db_article_answer.answer,
                    score=db_article_answer.score
                ) for db_article_answer in db_article_answers]
            ))
        
        return psychs_schma.PsychArticleQuestions(questions=questions_list)

    return None


def get_psych_question_statistics(db: Session, article_id: int) -> psychs_schma.PsychArticleQuestionStatistics:
    db_article_questions = db.query(psych_model.PsychArticleQuestions).filter(psych_model.PsychArticleQuestions.article_id == article_id).all()

    questions_list = []

    if db_article_questions:
        for index, db_article_question in enumerate(db_article_questions):

            db_article_answers = db.query(psych_model.PsychArticleAnswer).filter(psych_model.PsychArticleAnswer.question_id == db_article_question.id).all()
            question_attachment = db.query(psych_model.PsychArticleQuestionAttachment).filter(psych_model.PsychArticleQuestionAttachment.question_id == db_article_question.id).first()

            questions_list.append(psychs_schma.PsychArticleQuestionStatistic(
                index=index,
                question=db_article_question.question,
                description=db_article_question.description,
                attachment=psychs_schma.PsychArticleQuestionAttachment(
                    image=question_attachment.image,
                    video=question_attachment.video,
                    audio=question_attachment.audio
                ) if question_attachment else None,
                answers=[psychs_schma.PsychArticleAnswerStatistics(
                    answer=db_article_answer.answer,
                    score=db_article_answer.score,
                    count=10
                ) for db_article_answer in db_article_answers]
            ))
        
        return psychs_schma.PsychArticleQuestionStatistics(questions=questions_list)

    return None


def get_psych_owner(db: Session, article_id: int) -> int:
    db_article = db.query(psych_model.PsychArticle).filter(psych_model.PsychArticle.id == article_id).first()

    if not db_article:
        return None

    return db_article.author_id
    