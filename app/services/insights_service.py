from collections import Counter
from sqlalchemy.orm import Session
from app.db.models import (
    StudyPlan,
    JobAnalysis,
    InterviewQuestions,
    AnswerEvaluation,
    SkillInsight,
)


class InsightsService:
    def get_recurring_skill_gaps(self, db: Session):
        records = (
            db.query(SkillInsight)
            .filter(SkillInsight.skill_type == "gap")
            .order_by(SkillInsight.count.desc())
            .all()
        )

        return [
            {
                "skill": record.skill_name,
                "count": record.count,
            }
            for record in records
        ]

    def get_career_summary(self, db: Session):
        total_jobs_analyzed = db.query(JobAnalysis).count()
        total_questions_generated = db.query(InterviewQuestions).count()
        total_answers_evaluated = db.query(AnswerEvaluation).count()
        total_study_plans = db.query(StudyPlan).count()

        recurring_gaps = self.get_recurring_skill_gaps(db)
        top_gaps = recurring_gaps[:5]

        recommended_focus = [
            gap["skill"]
            for gap in top_gaps[:3]
        ]

        return {
            "total_jobs_analyzed": total_jobs_analyzed,
            "total_questions_generated": total_questions_generated,
            "total_answers_evaluated": total_answers_evaluated,
            "total_study_plans": total_study_plans,
            "top_skill_gaps": top_gaps,
            "recommended_focus": recommended_focus,
        }

    def get_top_strengths(self, db: Session):
        records = (
            db.query(SkillInsight)
            .filter(SkillInsight.skill_type == "strength")
            .order_by(SkillInsight.count.desc())
            .all()
        )

        return [
            {
                "strength": record.skill_name,
                "count": record.count,
            }
            for record in records
        ]
    
    def normalize_skill_name(self, skill_name: str) -> str:
        return skill_name.strip().lower()


    def update_skill_insight(self, db: Session, skill_name: str, skill_type: str):
        normalized_skill = self.normalize_skill_name(skill_name)

        if not normalized_skill:
            return None

        existing_skill = (
            db.query(SkillInsight)
            .filter(
                SkillInsight.skill_name == normalized_skill,
                SkillInsight.skill_type == skill_type,
            )
            .first()
        )

        if existing_skill:
            existing_skill.count += 1
        else:
            existing_skill = SkillInsight(
                skill_name=normalized_skill,
                skill_type=skill_type,
                count=1,
            )
            db.add(existing_skill)

        db.commit()
        db.refresh(existing_skill)

        return existing_skill


    def update_many_skill_insights(self, db: Session, skills: list[str], skill_type: str):
        updated_skills = []

        for skill in skills:
            updated_skill = self.update_skill_insight(
                db=db,
                skill_name=skill,
                skill_type=skill_type,
            )

            if updated_skill:
                updated_skills.append(updated_skill)

        return updated_skills
