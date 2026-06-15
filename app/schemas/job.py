from pydantic import BaseModel, Field
from typing import List


class JobAnalysisRequest(BaseModel):
    resume: str = Field(..., description="Candidate resume text")
    job_description: str = Field(..., description="Job description text")


class GenerateQuestionsRequest(BaseModel):
    resume: str = Field(..., description="Candidate resume text")
    job_description: str = Field(..., description="Job description text")

class EvaluateAnswerRequest(BaseModel):
    question: str = Field(..., description="Interview question")
    answer: str = Field(...,answer=" Candidate answer to evaluate")

class StudyPlanRequest(BaseModel):
    gaps: List[str] = Field(..., description="Skill gaps detected from the job analysis")
    target_role: str = Field(..., description="Target role or job position")
    available_days: int = Field(default=7, description="Number of days available to prepare")
