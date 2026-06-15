from app.services.llm_service import LLMService


class AnalysisService:
    def __init__(self):
        self.llm_service = LLMService()

    def analyze_job(self, resume: str, job_description: str) -> str:
        return self.llm_service.analyze_job(resume, job_description)

    def generate_questions(self, resume: str, job_description: str) -> str:
        return self.llm_service.generate_questions(resume, job_description)