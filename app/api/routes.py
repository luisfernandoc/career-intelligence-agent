from fastapi import APIRouter
from app.schemas.job import JobAnalysisRequest, GenerateQuestionsRequest, EvaluateAnswerRequest
from app.services.analysis_service import AnalysisService

router = APIRouter()

analysis_service = AnalysisService()


@router.post("/analyze-job")
def analyze_job(request: JobAnalysisRequest):
    result = analysis_service.analyze_job(
        resume=request.resume,
        job_description=request.job_description,
    )

    return {"analysis": result}


@router.post("/generate-questions")
def generate_questions(request: GenerateQuestionsRequest):
    result = analysis_service.generate_questions(
        resume=request.resume,
        job_description=request.job_description,
    )

    return {"questions": result}

@router.post("/evaluate-answer")
def evaluate_answer(request: EvaluateAnswerRequest):
    result = analysis_service.evaluate_answer(
        question=request.question,
        answer=request.answer,
    )

    return {"evaluation": result}
