from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    analysis_result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InterviewQuestions(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    resume = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    questions_result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    evaluation_result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    target_role = Column(String(255), nullable=False)
    gaps = Column(Text, nullable=False)
    study_plan_result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SkillInsight(Base):
    __tablename__ = "skill_insights"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    skill_type = Column(String(50), nullable=False)  # "strength" or "gap"
    count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False)
    source = Column(String(100), nullable=False,)
    chroma_id = Column(String(255), nullable=False, unique=True,)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),)
