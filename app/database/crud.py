from sqlalchemy.orm import Session

from app.database import models, schemas
from app.auth.hashing import hash_password

def create_user(db: Session, user: schemas.UserCreate):

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str):

    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

def get_user(db: Session, user_id: int):

    return (
        db.query(models.User)
        .filter(models.User.user_id == user_id)
        .first()
    )

def create_query(db: Session, query: schemas.UserQueryCreate):

    db_query = models.UserQuery(
        user_id=query.user_id,
        query_type=query.query_type,
        query_text=query.query_text
    )

    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    return db_query

def get_query(db: Session, query_id: int):

    return (
        db.query(models.UserQuery)
        .filter(models.UserQuery.query_id == query_id)
        .first()
    )

def save_ai_response(db: Session, response: schemas.AIResponseCreate):

    db_response = models.AIResponse(
        query_id=response.query_id,
        response_text=response.response_text,
        model_used=response.model_used
    )

    db.add(db_response)
    db.commit()
    db.refresh(db_response)

    return db_response

def save_quiz(
    db,
    query_id,
    question_text,
    option_a,
    option_b,
    option_c,
    option_d,
    correct_answer
):

    quiz = models.Quiz(
        query_id=query_id,
        question_text=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz

def save_summary(
    db,
    query_id,
    summary_text,
    summary_type
):

    summary = models.Summary(
        query_id=query_id,
        summary_text=summary_text,
        summary_type=summary_type
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary

def save_learning_path(
    db,
    query_id,
    topic,
    difficulty_level,
    recommended_resources
):

    path = models.LearningPath(
        query_id=query_id,
        topic=topic,
        difficulty_level=difficulty_level,
        recommended_resources=recommended_resources
    )

    db.add(path)
    db.commit()
    db.refresh(path)

    return path

def get_user_queries(db: Session, user_id: int):

    return (
        db.query(models.UserQuery)
        .filter(models.UserQuery.user_id == user_id)
        .all()
    )

def get_quizzes(db: Session, query_id: int):

    return (
        db.query(models.Quiz)
        .filter(models.Quiz.query_id == query_id)
        .all()
    )

def get_summaries(db: Session, query_id: int):

    return (
        db.query(models.Summary)
        .filter(models.Summary.query_id == query_id)
        .all()
    )

def get_learning_paths(db: Session, query_id: int):

    return (
        db.query(models.LearningPath)
        .filter(models.LearningPath.query_id == query_id)
        .all()
    )

def create_query(db, user_id, query_type, query_text):

    query = models.UserQuery(
        user_id=user_id,
        query_type=query_type,
        query_text=query_text
    )

    db.add(query)
    db.commit()
    db.refresh(query)

    return query

def create_ai_response(db, query_id, response_text, model_used):

    response = models.AIResponse(
        query_id=query_id,
        response_text=response_text,
        model_used=model_used
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    return response
def save_quiz_attempt(
    db,
    user_id,
    query_id,
    score,
    total_questions
):

    attempt = models.QuizAttempt(

        user_id=user_id,

        query_id=query_id,

        score=score,

        total_questions=total_questions

    )

    db.add(attempt)

    db.commit()

    db.refresh(attempt)

    return attempt
def save_history(db, user_id, task, prompt, response):

    history = models.History(

        user_id=user_id,
        task=task,
        prompt=prompt,
        response=response

    )

    db.add(history)

    db.commit()

    db.refresh(history)

    return history
def get_history(db, user_id):

    return (
        db.query(models.History)
        .filter(models.History.user_id == user_id)
        .order_by(models.History.created_at.desc())
        .limit(20)
        .all()
    )
def get_dashboard_stats(db, user_id):

    return {

        "questions":
        db.query(models.History)
        .filter_by(user_id=user_id, task="question")
        .count(),

        "quizzes":
        db.query(models.History)
        .filter_by(user_id=user_id, task="quiz")
        .count(),

        "summaries":
        db.query(models.History)
        .filter_by(user_id=user_id, task="summary")
        .count(),

        "learning_paths":
        db.query(models.History)
        .filter_by(user_id=user_id, task="learning")
        .count()

    }