from dotenv import load_dotenv
from app.providers.provider_factory import get_llm_provider

load_dotenv()


class LLMService:
    def __init__(self):
        self.provider = get_llm_provider()

    def analyze_job(self, resume: str, job_description: str) -> str:
        system_prompt = "You are an expert career and technical interview advisor."

        user_prompt = f"""
You are a career intelligence assistant.

Analyze the candidate resume against the job description.

Return:
- Match score from 0 to 100
- Main strengths
- Skill gaps
- Interview risks
- Short recommendation

Resume:
{resume}

Job Description:
{job_description}
"""

        return self.provider.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
        )

    def generate_questions(self, resume: str, job_description: str) -> str:
        system_prompt = "You generate practical interview questions."

        user_prompt = f"""
You are a technical interviewer.

Based on the resume and job description, generate interview questions.

Return:
- 5 technical questions
- 3 behavioral questions
- 2 project-based questions

Resume:
{resume}

Job Description:
{job_description}
"""

        return self.provider.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
        )
    
    def evaluate_answer(self, question: str, answer: str) -> str:
        system_prompt = "You are an expert technical interviewer. Evaluate interview answers fairly and professionally."

        user_prompt = f"""
Question:

{question}

Candidate Answer:

{answer}

Evaluate:

1. Score from 1 to 10
2. Strengths
3. Weaknesses
4. Missing concepts
5. Improved answer

Be constructive and specific.
"""

        return self.provider.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
        )
