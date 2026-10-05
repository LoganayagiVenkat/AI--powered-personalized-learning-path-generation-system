import json
import logging
from sqlalchemy.orm import Session
from backend.models.models import (
    User, StudentProfile, CareerGoal, Topic, Recommendation, LearningPathTopic, LearningPath
)

logger = logging.getLogger("learning_path.recommendation")

CURATED_PROJECTS = [
    {
        "title": "End-to-End Customer Churn Prediction Engine",
        "category": "AI/ML",
        "type": "project",
        "difficulty": "Intermediate",
        "skills": ["Python Programming", "Machine Learning", "Data Visualization"],
        "reasoning": "High-impact portfolio project demonstrating supervised classification, feature engineering, and ROC-AUC business evaluation."
    },
    {
        "title": "Real-Time NLP Semantic Search Engine with Embeddings",
        "category": "AI/ML",
        "type": "project",
        "difficulty": "Advanced",
        "skills": ["Natural Language Processing (NLP)", "Deep Learning & Neural Networks"],
        "reasoning": "Directly develops vector similarity and transformer skills required for modern AI Engineer roles."
    },
    {
        "title": "Automated Financial Time Series Forecast Dashboard",
        "category": "Data",
        "type": "project",
        "difficulty": "Intermediate",
        "skills": ["Python Programming", "Statistics & Probability", "SQL & Databases"],
        "reasoning": "Strengthens statistical inference, data wrangling with SQL, and interactive web dashboard visualization."
    },
    {
        "title": "Full-Stack AI Learning Assistant with Microservices",
        "category": "Web",
        "type": "project",
        "difficulty": "Advanced",
        "skills": ["JavaScript & React", "REST API Architecture", "Python Programming"],
        "reasoning": "Showcases end-to-end full stack architecture integrating responsive React interfaces with Python AI inference endpoints."
    }
]

def generate_recommendations(db: Session, user_id: int) -> list:
    """
    Generate tailored multi-modal recommendations:
    - Next Priority Topic
    - Hands-on Capstone Projects matching target career
    - Interactive Quizzes for active topics
    - Practice Coding Exercises
    """
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    path = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()

    recommendations = []

    # 1. Recommend Active / Pending Topic from Learning Path
    if path:
        in_prog_lpt = db.query(LearningPathTopic).filter(
            LearningPathTopic.learning_path_id == path.id,
            LearningPathTopic.status.in_(["in_progress", "review_needed"])
        ).first()

        if in_prog_lpt and in_prog_lpt.topic:
            topic = in_prog_lpt.topic
            recommendations.append({
                "item_type": "topic",
                "item_title": topic.title,
                "item_id": topic.id,
                "badge": "Active Priority",
                "score": 0.98,
                "difficulty": topic.difficulty,
                "reasoning": f"Currently active module on your personalized path: {in_prog_lpt.recommended_reason}",
                "action_url": f"/learn/{topic.id}"
            })

            # Recommend Quiz for this topic
            recommendations.append({
                "item_type": "quiz",
                "item_title": f"{topic.title} Mastery Evaluation",
                "item_id": topic.id,
                "badge": "Verify Skill",
                "score": 0.92,
                "difficulty": topic.difficulty,
                "reasoning": f"Complete this 10-minute assessment to unlock downstream modules and validate your comprehension.",
                "action_url": f"/quiz/{topic.id}"
            })

    # 2. Recommend Projects tailored to Career Goal
    career_title = profile.target_job_role if profile else "Data Scientist"
    for proj in CURATED_PROJECTS:
        # Check alignment with career title
        is_relevant = False
        if "Data" in career_title and proj["category"] in ["AI/ML", "Data"]:
            is_relevant = True
        elif "AI" in career_title and proj["category"] in ["AI/ML"]:
            is_relevant = True
        elif "Web" in career_title or "Full" in career_title:
            is_relevant = True

        if is_relevant:
            recommendations.append({
                "item_type": "project",
                "item_title": proj["title"],
                "item_id": None,
                "badge": f"{proj['difficulty']} Project",
                "score": 0.88,
                "difficulty": proj["difficulty"],
                "reasoning": proj["reasoning"],
                "action_url": "/projects"
            })

    # 3. Recommend Specialized External Resources
    recommendations.append({
        "item_type": "course",
        "item_title": "Deep Learning Specialization (Coursera / DeepLearning.AI)",
        "item_id": None,
        "badge": "Recommended Course",
        "score": 0.85,
        "difficulty": "Intermediate-Advanced",
        "reasoning": "Industry-standard curriculum covering neural networks, hyperparameter tuning, and sequence models.",
        "action_url": "https://www.deeplearning.ai/"
    })

    return recommendations
