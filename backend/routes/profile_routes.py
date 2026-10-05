import json
import logging
from flask import Blueprint, request, jsonify
from backend.database.db import get_db
from backend.models.models import User, StudentProfile, CareerGoal, Skill, StudentSkill

logger = logging.getLogger("learning_path.profile")
profile_bp = Blueprint("profile", __name__)

def get_current_user_id():
    # Helper to resolve user_id from query param, headers, or default to demo user (id=1)
    uid = request.headers.get("X-User-Id") or request.args.get("user_id")
    try:
        return int(uid) if uid else 1
    except Exception:
        return 1

@profile_bp.route("/api/profile", methods=["GET"])
def get_profile():
    user_id = get_current_user_id()
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            # Fallback to first user
            user = db.query(User).first()
        if not user:
            return jsonify({"error": "No user found"}), 404

        profile = user.profile
        career = profile.career_goal if profile else None

        skills_list = []
        for ss in user.skills:
            if ss.skill:
                skills_list.append({
                    "skill_id": ss.skill.id,
                    "name": ss.skill.name,
                    "category": ss.skill.category,
                    "current_level": ss.current_level,
                    "confidence_score": ss.confidence_score,
                    "verified": ss.verified_by_assessment
                })

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "education_level": profile.education_level if profile else "Undergraduate",
            "experience_level": profile.experience_level if profile else "Beginner",
            "interests": profile.interests if profile else "Machine Learning, Python, Data Science",
            "target_job_role": profile.target_job_role if profile else "Data Scientist",
            "overall_skill_level": profile.overall_skill_level if profile else "Beginner",
            "bio": profile.bio if profile else "",
            "streak_days": profile.streak_days if profile else 1,
            "total_learning_minutes": profile.total_learning_minutes if profile else 0,
            "career_goal": {
                "id": career.id if career else None,
                "title": career.title if career else "Data Scientist",
                "target_role": career.target_role if career else "Data Scientist",
                "description": career.description if career else ""
            },
            "skills": skills_list
        }), 200
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        return jsonify({"error": "Failed to fetch profile"}), 500
    finally:
        db.close()

@profile_bp.route("/api/profile", methods=["PUT"])
def update_profile():
    user_id = get_current_user_id()
    data = request.get_json() or {}
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = db.query(User).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        profile = user.profile
        if not profile:
            profile = StudentProfile(user_id=user.id)
            db.add(profile)

        if "name" in data and data["name"]:
            user.name = data["name"].strip()
        if "education_level" in data:
            profile.education_level = data["education_level"]
        if "experience_level" in data:
            profile.experience_level = data["experience_level"]
        if "interests" in data:
            profile.interests = data["interests"]
        if "target_job_role" in data:
            profile.target_job_role = data["target_job_role"]
        if "bio" in data:
            profile.bio = data["bio"]
        if "career_goal_id" in data and data["career_goal_id"]:
            profile.career_goal_id = int(data["career_goal_id"])

        # Update skills if provided
        if "skills" in data and isinstance(data["skills"], list):
            for sk_item in data["skills"]:
                sk_name = sk_item.get("name")
                level = sk_item.get("current_level", "Beginner")
                if not sk_name:
                    continue
                skill = db.query(Skill).filter(Skill.name == sk_name).first()
                if skill:
                    st_skill = db.query(StudentSkill).filter(
                        StudentSkill.user_id == user.id,
                        StudentSkill.skill_id == skill.id
                    ).first()
                    if not st_skill:
                        st_skill = StudentSkill(user_id=user.id, skill_id=skill.id)
                        db.add(st_skill)
                    st_skill.current_level = level

        db.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating profile: {e}")
        return jsonify({"error": "Failed to update profile"}), 500
    finally:
        db.close()

@profile_bp.route("/api/career-goals", methods=["GET"])
def get_career_goals():
    db = next(get_db())
    try:
        goals = db.query(CareerGoal).all()
        result = []
        for g in goals:
            result.append({
                "id": g.id,
                "title": g.title,
                "target_role": g.target_role,
                "description": g.description,
                "required_skills": json.loads(g.required_skills_json or "[]")
            })
        return jsonify(result), 200
    finally:
        db.close()

@profile_bp.route("/api/skills", methods=["GET"])
def get_all_skills():
    db = next(get_db())
    try:
        skills = db.query(Skill).all()
        return jsonify([{
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "description": s.description
        } for s in skills]), 200
    finally:
        db.close()
