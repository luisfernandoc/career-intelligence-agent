from pydantic import BaseModel, Field


class JobAnalysisRequest(BaseModel):
    resume: str = Field(..., description="Candidate resume text")
    job_description: str = Field(..., description="Job description text")


class GenerateQuestionsRequest(BaseModel):
    resume: str = Field(..., description="Candidate resume text")
    job_description: str = Field(..., description="Job description text")

class EvaluateAnswerRequest(BaseModel):
    question: str = Field(..., description="Interview question")
    answer: str = Field(...,answer=" Candidate answer to evaluate")
