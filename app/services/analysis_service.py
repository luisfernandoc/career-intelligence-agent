import json
from app.services.llm_service import LLMService


class AnalysisService:
    def __init__(self):
        self.llm_service = LLMService()

    def analyze_job(self, resume: str, job_description: str):
        raw_result = self.llm_service.analyze_job(
            resume=resume,
            job_description=job_description,
        )

        try:
            return json.loads(raw_result)
        except json.JSONDecodeError:
            return {
                "match_score": None,
                "strengths": [],
                "gaps": [],
                "interview_risks": ["Could not parse LLM response as JSON"],
                "recommendation": raw_result,
            }

    def generate_questions(self, resume: str, job_description: str) -> str:
        return self.llm_service.generate_questions(resume, job_description)

    def evaluate_answer(self, question: str, answer: str) -> str:
        return self.llm_service.evaluate_answer(question, answer)
    
    def generate_study_plan(self, gaps: list[str], target_role: str, available_days: int,) -> str:
        return self.llm_service.generate_study_plan(gaps=gaps, target_role=target_role, available_days=available_days,)
