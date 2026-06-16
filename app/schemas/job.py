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

class UploadDocumentRequest(BaseModel):
    title: str = Field(..., description="Document title", example="Luis Resume")
    content: str = Field(..., description="Document content to store in career memory")
    document_type: str = Field(default="general", description="Type of document: resume, job_description, interview_notes, project, certification")

class AskCareerMemoryRequest(BaseModel):
    question: str = Field(..., description="Question to ask against the career memory", example="What evidence do I have to prove FastAPI experience?")
