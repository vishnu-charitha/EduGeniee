from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# ---------- USER ----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- USER QUERY ----------

class UserQueryCreate(BaseModel):
    user_id: int
    query_type: str
    query_text: str


class UserQueryResponse(BaseModel):
    query_id: int
    user_id: int
    query_type: str
    query_text: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- AI RESPONSE ----------

class AIResponseCreate(BaseModel):
    query_id: int
    response_text: str
    model_used: str


class AIResponseResponse(BaseModel):
    response_id: int
    query_id: int
    response_text: str
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- QUIZ ----------

class QuizCreate(BaseModel):
    query_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str


class QuizResponse(BaseModel):
    quiz_id: int
    query_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- SUMMARY ----------

class SummaryCreate(BaseModel):
    query_id: int
    summary_text: str
    summary_type: str


class SummaryResponse(BaseModel):
    summary_id: int
    query_id: int
    summary_text: str
    summary_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- LEARNING PATH ----------

class LearningPathCreate(BaseModel):
    query_id: int
    topic: str
    difficulty_level: str
    recommended_resources: str


class LearningPathResponse(BaseModel):
    path_id: int
    query_id: int
    topic: str
    difficulty_level: str
    recommended_resources: str
    created_at: datetime

    class Config:
        from_attributes = True

