import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging
from werkzeug.security import generate_password_hash
from backend.database.db import get_db
from backend.models.models import (
    User, StudentProfile, CareerGoal, Skill, StudentSkill
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed_accounts")

DEMO_STUDENTS = [
    {
        "name": "Alex Morgan",
        "email": "alex.morgan@example.com",
        "target_role": "Data Scientist",
        "overall_skill_level": "Beginner",
        "education": "Undergraduate",
        "experience": "Beginner",
        "interests": "Machine Learning, Data Science, Python, Predictive Analytics",
        "bio": "Aspiring Data Scientist with foundational Python looking to master machine learning pipelines.",
        "streak": 4,
        "minutes": 180,
        "goal_role": "Data Scientist",
        "skills": [
            ("Python Programming", "Beginner", 0.60),
            ("SQL & Databases", "Beginner", 0.40),
            ("Statistics & Probability", "Beginner", 0.35),
        ]
    },
    {
        "name": "Priya Sharma",
        "email": "priya.sharma@example.com",
        "target_role": "AI / ML Engineer",
        "overall_skill_level": "Intermediate",
        "education": "Master's Degree",
        "experience": "Intermediate",
        "interests": "Deep Learning, PyTorch, Neural Networks, Computer Vision, Transformers",
        "bio": "Graduate researcher in AI/ML focusing on deep learning architectures and NLP systems.",
        "streak": 12,
        "minutes": 490,
        "goal_role": "AI / ML Engineer",
        "skills": [
            ("Python Programming", "Advanced", 0.90),
            ("Machine Learning", "Intermediate", 0.78),
            ("Deep Learning & Neural Networks", "Intermediate", 0.72),
            ("Linear Algebra & Calculus", "Intermediate", 0.75),
            ("Natural Language Processing (NLP)", "Beginner", 0.60),
        ]
    },
    {
        "name": "Marcus Chen",
        "email": "marcus.chen@example.com",
        "target_role": "Full Stack Developer",
        "overall_skill_level": "Advanced",
        "education": "Bachelor's in CS",
        "experience": "Advanced",
        "interests": "React, TypeScript, Node.js, SQL, Cloud Architecture, Microservices",
        "bio": "Full-stack software engineer building distributed cloud web applications and REST APIs.",
        "streak": 21,
        "minutes": 850,
        "goal_role": "Full Stack Developer",
        "skills": [
            ("JavaScript & React", "Advanced", 0.92),
            ("REST API Architecture", "Advanced", 0.88),
            ("Python Programming", "Intermediate", 0.80),
            ("SQL & Databases", "Intermediate", 0.75),
        ]
    },
    {
        "name": "Aisha Patel",
        "email": "aisha.patel@example.com",
        "target_role": "Data Scientist",
        "overall_skill_level": "Beginner",
        "education": "Bootcamp / Self-Taught",
        "experience": "Beginner",
        "interests": "Data Analytics, Statistics, Python, Pandas, Tableau",
        "bio": "Data enthusiast transitioning into predictive analytics and business intelligence.",
        "streak": 2,
        "minutes": 75,
        "goal_role": "Data Scientist",
        "skills": [
            ("Statistics & Probability", "Intermediate", 0.65),
            ("Data Visualization", "Intermediate", 0.70),
            ("Python Programming", "Beginner", 0.35),
        ]
    }
]

def seed_demo_accounts():
    db = next(get_db())
    try:
        goals = {cg.target_role: cg for cg in db.query(CareerGoal).all()}
        skills = {s.name: s for s in db.query(Skill).all()}
        
        for acc in DEMO_STUDENTS:
            user = db.query(User).filter(User.email == acc["email"]).first()
            if not user:
                user = User(
                    name=acc["name"],
                    email=acc["email"],
                    password_hash=generate_password_hash("password123")
                )
                db.add(user)
                db.flush()
                logger.info(f"Created student user: {acc['name']} (ID: {user.id})")
            else:
                user.name = acc["name"]
                logger.info(f"Found existing student user: {acc['name']} (ID: {user.id})")

            target_goal = goals.get(acc["goal_role"])
            if not user.profile:
                profile = StudentProfile(
                    user_id=user.id,
                    education_level=acc["education"],
                    experience_level=acc["experience"],
                    interests=acc["interests"],
                    career_goal_id=target_goal.id if target_goal else None,
                    target_job_role=acc["target_role"],
                    overall_skill_level=acc["overall_skill_level"],
                    bio=acc["bio"],
                    streak_days=acc["streak"],
                    total_learning_minutes=acc["minutes"]
                )
                db.add(profile)
            else:
                user.profile.education_level = acc["education"]
                user.profile.experience_level = acc["experience"]
                user.profile.interests = acc["interests"]
                user.profile.target_job_role = acc["target_role"]
                user.profile.overall_skill_level = acc["overall_skill_level"]
                user.profile.bio = acc["bio"]
                user.profile.streak_days = acc["streak"]
                user.profile.total_learning_minutes = acc["minutes"]
                if target_goal:
                    user.profile.career_goal_id = target_goal.id

            # Populate initial skills
            for skill_name, lvl, conf in acc["skills"]:
                s_obj = skills.get(skill_name)
                if s_obj:
                    ss = db.query(StudentSkill).filter(
                        StudentSkill.user_id == user.id,
                        StudentSkill.skill_id == s_obj.id
                    ).first()
                    if not ss:
                        ss = StudentSkill(
                            user_id=user.id,
                            skill_id=s_obj.id,
                            current_level=lvl,
                            confidence_score=conf,
                            verified_by_assessment=True
                        )
                        db.add(ss)
                    else:
                        ss.current_level = lvl
                        ss.confidence_score = conf
                        ss.verified_by_assessment = True

        db.commit()
        logger.info("Successfully seeded all 4 demo student profiles!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding demo accounts: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_accounts()
