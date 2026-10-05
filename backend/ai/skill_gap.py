import json
import logging
from sqlalchemy.orm import Session
from backend.models.models import (
    User, StudentProfile, CareerGoal, Skill, StudentSkill, Topic, SkillGap
)

logger = logging.getLogger("learning_path.skill_gap")

LEVEL_MAP = {
    "none": 0,
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

REVERSE_LEVEL_MAP = {
    0: "None",
    1: "Beginner",
    2: "Intermediate",
    3: "Advanced"
}

# Mapping skills to best corresponding learning topics
SKILL_TO_TOPIC_MAP = {
    "Python Programming": "Python Programming Fundamentals",
    "SQL & Databases": "SQL & Relational Database Engineering",
    "Statistics & Probability": "Probability & Descriptive Statistics",
    "Linear Algebra & Calculus": "Mathematics & Linear Algebra for AI",
    "Data Visualization": "Exploratory Data Analysis & Visualization",
    "Machine Learning": "Supervised Machine Learning Algorithms",
    "Deep Learning & Neural Networks": "Deep Learning & Neural Networks",
    "Natural Language Processing (NLP)": "Natural Language Processing (NLP) & Transformers"
}

def analyze_student_skill_gaps(db: Session, user_id: int) -> dict:
    """
    Compare student's current skills against target career requirements.
    Calculates gaps, updates database records, and returns structured analytics.
    """
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    career_goal = None
    if profile and profile.career_goal_id:
        career_goal = db.query(CareerGoal).filter(CareerGoal.id == profile.career_goal_id).first()
    
    if not career_goal:
        career_goal = db.query(CareerGoal).first()

    if not career_goal or not career_goal.required_skills_json:
        return {"gaps": [], "readiness_score": 0, "career_goal": "Not Defined"}

    try:
        required_skills = json.loads(career_goal.required_skills_json)
    except Exception:
        required_skills = []

    # Get student's current assessed / reported skills
    student_skills_records = db.query(StudentSkill).filter(StudentSkill.user_id == user_id).all()
    user_skill_levels = {
        ss.skill.name.lower(): (ss.current_level, ss.confidence_score)
        for ss in student_skills_records if ss.skill
    }

    gaps_result = []
    total_required_points = 0
    total_earned_points = 0

    # Delete previous snapshot of gaps for this user
    db.query(SkillGap).filter(SkillGap.user_id == user_id).delete()

    for item in required_skills:
        skill_name = item.get("skill_name", "")
        req_level_str = item.get("required_level", "Intermediate")
        req_val = LEVEL_MAP.get(req_level_str.lower(), 2)
        weight = item.get("weight", 0.2)

        curr_level_str, confidence = user_skill_levels.get(skill_name.lower(), ("Beginner", 0.3))
        curr_val = LEVEL_MAP.get(curr_level_str.lower(), 1)

        gap_diff = req_val - curr_val
        total_required_points += req_val * weight
        total_earned_points += min(curr_val, req_val) * weight

        if gap_diff >= 2:
            gap_status = "Critical"
        elif gap_diff == 1:
            gap_status = "Moderate"
        elif gap_diff == 0:
            gap_status = "Met"
        else:
            gap_status = "Advanced"

        # Find or link corresponding skill & topic
        skill_obj = db.query(Skill).filter(Skill.name == skill_name).first()
        topic_title = SKILL_TO_TOPIC_MAP.get(skill_name)
        topic_obj = db.query(Topic).filter(Topic.title == topic_title).first() if topic_title else None

        if skill_obj:
            gap_record = SkillGap(
                user_id=user_id,
                skill_id=skill_obj.id,
                target_career_id=career_goal.id,
                required_level=req_level_str,
                current_level=curr_level_str,
                gap_status=gap_status,
                gap_score=float(max(0, gap_diff)),
                recommended_topic_id=topic_obj.id if topic_obj else None
            )
            db.add(gap_record)

        gaps_result.append({
            "skill_name": skill_name,
            "category": skill_obj.category if skill_obj else "General",
            "required_level": req_level_str,
            "required_val": req_val,
            "current_level": curr_level_str,
            "current_val": curr_val,
            "gap_diff": gap_diff,
            "gap_status": gap_status,
            "recommended_topic": topic_obj.title if topic_obj else "Foundation Course",
            "recommended_topic_id": topic_obj.id if topic_obj else None,
            "confidence_score": round(confidence, 2)
        })

    db.commit()

    readiness_percentage = round((total_earned_points / max(total_required_points, 1.0)) * 100, 1)

    return {
        "target_career": career_goal.title,
        "target_role": career_goal.target_role,
        "career_description": career_goal.description,
        "readiness_percentage": readiness_percentage,
        "critical_gaps_count": sum(1 for g in gaps_result if g["gap_status"] == "Critical"),
        "moderate_gaps_count": sum(1 for g in gaps_result if g["gap_status"] == "Moderate"),
        "met_skills_count": sum(1 for g in gaps_result if g["gap_status"] in ["Met", "Advanced"]),
        "gaps": gaps_result
    }
