import logging
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db import get_db
from backend.models.models import User, StudentProfile, CareerGoal

logger = logging.getLogger("learning_path.auth")
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    db = next(get_db())
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return jsonify({"error": "An account with this email already exists"}), 409

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.add(user)
        db.flush()

        # Link default career goal
        default_goal = db.query(CareerGoal).first()
        profile = StudentProfile(
            user_id=user.id,
            education_level=data.get("education_level", "Undergraduate"),
            experience_level=data.get("experience_level", "Beginner"),
            interests=data.get("interests", "Machine Learning, Data Science, Python"),
            career_goal_id=default_goal.id if default_goal else None,
            target_job_role=data.get("target_job_role", "Data Scientist"),
            overall_skill_level="Beginner",
            bio=data.get("bio", f"Aspiring {data.get('target_job_role', 'Data Scientist')} looking to build practical skills.")
        )
        db.add(profile)
        db.commit()

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "target_job_role": profile.target_job_role
            }
        }), 201
    except Exception as e:
        db.rollback()
        logger.error(f"Registration error: {e}")
        return jsonify({"error": "Registration failed"}), 500
    finally:
        db.close()

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = next(get_db())
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid email or password"}), 401

        profile = user.profile
        return jsonify({
            "message": "Login successful",
            "token": f"mock-jwt-token-user-{user.id}",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "education_level": profile.education_level if profile else "Undergraduate",
                "experience_level": profile.experience_level if profile else "Beginner",
                "target_job_role": profile.target_job_role if profile else "Data Scientist",
                "overall_skill_level": profile.overall_skill_level if profile else "Beginner"
            }
        }), 200
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500
    finally:
        db.close()

@auth_bp.route("/api/auth/demo-accounts", methods=["GET"])
def get_demo_accounts():
    db = next(get_db())
    try:
        users = db.query(User).all()
        if not users:
            from backend.database.seed_accounts import seed_demo_accounts
            seed_demo_accounts()
            users = db.query(User).all()

        accounts = []
        for u in users:
            p = u.profile
            accounts.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "target_job_role": p.target_job_role if p else "Data Scientist",
                "education_level": p.education_level if p else "Undergraduate",
                "experience_level": p.experience_level if p else "Beginner",
                "overall_skill_level": p.overall_skill_level if p else "Beginner",
                "streak_days": p.streak_days if p else 1,
                "total_learning_minutes": p.total_learning_minutes if p else 0,
                "bio": p.bio if p else ""
            })

        return jsonify({"accounts": accounts}), 200
    except Exception as e:
        logger.error(f"Error fetching accounts: {e}")
        return jsonify({"error": "Failed to load accounts"}), 500
    finally:
        db.close()

@auth_bp.route("/api/auth/switch", methods=["POST"])
def switch_account():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    email = data.get("email")

    db = next(get_db())
    try:
        user = None
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
        elif email:
            user = db.query(User).filter(User.email == email.strip().lower()).first()

        if not user:
            return jsonify({"error": "Target account not found"}), 404

        p = user.profile
        return jsonify({
            "message": f"Successfully switched to {user.name}",
            "token": f"mock-jwt-token-user-{user.id}",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "education_level": p.education_level if p else "Undergraduate",
                "experience_level": p.experience_level if p else "Beginner",
                "target_job_role": p.target_job_role if p else "Data Scientist",
                "overall_skill_level": p.overall_skill_level if p else "Beginner"
            }
        }), 200
    except Exception as e:
        logger.error(f"Account switch error: {e}")
        return jsonify({"error": "Account switch failed"}), 500
    finally:
        db.close()

