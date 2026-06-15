import json
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.schemas.job import JobAnalysisRequest, GenerateQuestionsRequest, EvaluateAnswerRequest, StudyPlanRequest, UploadDocumentRequest, AskCareerMemoryRequest
from app.services.memory_service import MemoryService
from app.services.analysis_service import AnalysisService
from app.services.insights_service import InsightsService
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import (
    JobAnalysis,
    InterviewQuestions,
    AnswerEvaluation,
    StudyPlan,
)

router = APIRouter()

analysis_service = AnalysisService()
insights_service = InsightsService()
memory_service = MemoryService()


@router.post("/analyze-job")
def analyze_job(request: JobAnalysisRequest, db: Session = Depends(get_db)):
    result = analysis_service.analyze_job(
        resume=request.resume,
        job_description=request.job_description,
    )

    record = JobAnalysis(
        resume=request.resume,
        job_description=request.job_description,
        analysis_result=json.dumps(result),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    strengths = result.get("strengths", [])
    gaps = result.get("gaps", [])

    insights_service.update_many_skill_insights(
        db=db,
        skills=strengths,
        skill_type="strength",
    )

    insights_service.update_many_skill_insights(
        db=db,
        skills=gaps,
        skill_type="gap",
    )

    return {
        "id": record.id,
        "analysis": result
    }


@router.post("/generate-questions")
def generate_questions(request: GenerateQuestionsRequest, db: Session = Depends(get_db)):
    result = analysis_service.generate_questions(
        resume=request.resume,
        job_description=request.job_description,
    )

    record = InterviewQuestions(
        resume=request.resume,
        job_description=request.job_description,
        questions_result=result,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "questions": result
    }

@router.post("/evaluate-answer")
def evaluate_answer(request: EvaluateAnswerRequest, db: Session = Depends(get_db)):
    result = analysis_service.evaluate_answer(
        question=request.question,
        answer=request.answer,
    )

    record = AnswerEvaluation(
        question=request.question,
        answer=request.answer,
        evaluation_result=result,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "evaluation": result
    }

@router.post("/study-plan")
def generate_study_plan(request: StudyPlanRequest, db: Session = Depends(get_db)):
    result = analysis_service.generate_study_plan(
        gaps=request.gaps,
        target_role=request.target_role,
        available_days=request.available_days,
    )

    record = StudyPlan(
        target_role=request.target_role,
        gaps=", ".join(request.gaps),
        study_plan_result=result,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "study_plan": result,
    }

@router.get("/history/job-analyses")
def get_job_analyses(db: Session = Depends(get_db)):
    records = db.query(JobAnalysis).order_by(JobAnalysis.created_at.desc()).all()

    return records


@router.get("/history/questions")
def get_generated_questions(db: Session = Depends(get_db)):
    records = db.query(InterviewQuestions).order_by(InterviewQuestions.created_at.desc()).all()

    return records


@router.get("/history/evaluations")
def get_answer_evaluations(db: Session = Depends(get_db)):
    records = db.query(AnswerEvaluation).order_by(AnswerEvaluation.created_at.desc()).all()

    return records


@router.get("/history/study-plans")
def get_study_plans(db: Session = Depends(get_db)):
    records = db.query(StudyPlan).order_by(StudyPlan.created_at.desc()).all()

    return records

@router.get("/insights/skill-gaps")
def get_skill_gap_insights(db: Session = Depends(get_db)):
    recurring_gaps = insights_service.get_recurring_skill_gaps(db)

    return {
        "recurring_gaps": recurring_gaps
    }

@router.get("/insights/career-summary")
def get_career_summary(db: Session = Depends(get_db)):
    return insights_service.get_career_summary(db)


@router.get("/insights/top-strengths")
def get_top_strengths(db: Session = Depends(get_db)):
    top_strengths = insights_service.get_top_strengths(db)

    return {
        "top_strengths": top_strengths
    }

@router.post("/upload-document")
def upload_document(request: UploadDocumentRequest):
    return memory_service.upload_document(
        title=request.title,
        content=request.content,
        document_type=request.document_type,
    )


@router.post("/ask-career-memory")
def ask_career_memory(request: AskCareerMemoryRequest):
    return memory_service.ask_career_memory(
        question=request.question,
    )

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...), document_type: str = Form(default="general")):
    content = await file.read()

    return memory_service.upload_file(
        file_name=file.filename,
        content=content,
        document_type=document_type,
    )
