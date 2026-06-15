from fastapi import APIRouter
from app.schemas.job import JobAnalysisRequest, GenerateQuestionsRequest
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