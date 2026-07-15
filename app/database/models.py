from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    DateTime,
    ForeignKey
)

from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    queries = relationship(
        "UserQuery",
        back_populates="user",
        cascade="all, delete"
    )
class UserQuery(Base):
    __tablename__ = "user_queries"

    query_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    query_type = Column(String(50), nullable=False)
    query_text = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="queries")

    ai_response = relationship(
        "AIResponse",
        uselist=False,
        back_populates="query",
        cascade="all, delete"
    )

    quizzes = relationship(
        "Quiz",
        back_populates="query",
        cascade="all, delete"
    )

    summaries = relationship(
        "Summary",
        back_populates="query",
        cascade="all, delete"
    )

    learning_paths = relationship(
        "LearningPath",
        back_populates="query",
        cascade="all, delete"
    )
class AIResponse(Base):
    __tablename__ = "ai_responses"

    response_id = Column(Integer, primary_key=True)

    query_id = Column(
        Integer,
        ForeignKey("user_queries.query_id", ondelete="CASCADE"),
        unique=True
    )

    response_text = Column(Text, nullable=False)

    model_used = Column(String(50))

    created_at = Column(TIMESTAMP, server_default=func.now())

    query = relationship(
        "UserQuery",
        back_populates="ai_response"
    )
class Quiz(Base):
    __tablename__ = "quizzes"

    quiz_id = Column(Integer, primary_key=True)

    query_id = Column(
        Integer,
        ForeignKey("user_queries.query_id", ondelete="CASCADE")
    )

    question_text = Column(Text, nullable=False)

    option_a = Column(Text)
    option_b = Column(Text)
    option_c = Column(Text)
    option_d = Column(Text)

    correct_answer = Column(String(5))

    created_at = Column(TIMESTAMP, server_default=func.now())

    query = relationship(
        "UserQuery",
        back_populates="quizzes"
    )
class Summary(Base):
    __tablename__ = "summaries"

    summary_id = Column(Integer, primary_key=True)

    query_id = Column(
        Integer,
        ForeignKey("user_queries.query_id", ondelete="CASCADE")
    )

    summary_text = Column(Text, nullable=False)

    summary_type = Column(String(30))

    created_at = Column(TIMESTAMP, server_default=func.now())

    query = relationship(
        "UserQuery",
        back_populates="summaries"
    )
class LearningPath(Base):
    __tablename__ = "learning_paths"

    path_id = Column(Integer, primary_key=True)

    query_id = Column(
        Integer,
        ForeignKey("user_queries.query_id", ondelete="CASCADE")
    )

    topic = Column(String(150), nullable=False)

    difficulty_level = Column(String(30))

    recommended_resources = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())

    query = relationship(
        "UserQuery",
        back_populates="learning_paths"
    )
class QuizAttempt(Base):

    __tablename__ = "quiz_attempts"

    attempt_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    query_id = Column(
    Integer,
    ForeignKey("user_queries.query_id")
)

    score = Column(Integer)

    total_questions = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    task = Column(String(50))

    prompt = Column(Text)

    response = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)