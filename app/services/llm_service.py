from dotenv import load_dotenv
from app.providers.provider_factory import get_llm_provider

load_dotenv()


class LLMService:
    def __init__(self):
        self.provider = get_llm_provider()

    def analyze_job(self, resume: str, job_description: str) -> str:
        system_prompt = """
    You are an expert career and technical interview advisor.

    You must return ONLY valid JSON.
    Do not include markdown.
    Do not include explanations outside the JSON.
    """

        user_prompt = f"""
    Analyze the candidate resume against the job description.

    Return this exact JSON structure:

    {{
    "match_score": 0,
    "strengths": [],
    "gaps": [],
    "interview_risks": [],
    "recommendation": ""
    }}

    Rules:
    - match_score must be a number from 0 to 100
    - strengths must be a list of short skill names
    - gaps must be a list of short skill names
    - interview_risks must be a list of short risks
    - recommendation must be a short paragraph

    Resume:
    {resume}

    Job Description:
    {job_description}
    """

        return self.provider.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
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
    
    def generate_study_plan(self, gaps: list[str], target_role: str, available_days: int,) -> str:
        system_prompt = """
You are an expert career coach and technical interview preparation advisor.
Create realistic, focused and practical study plans.
"""

        user_prompt = f"""
Create a study plan for the candidate.

Target role:
{target_role}

Skill gaps:
{", ".join(gaps)}

Available days:
{available_days}

Return:
1. Main preparation priorities
2. Daily study plan
3. Practice exercises
4. Suggested mini-project improvements
5. Final recommendation

Keep it realistic and focused.
"""

        return self.provider.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
        )
