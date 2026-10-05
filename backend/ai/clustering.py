import numpy as np
from sklearn.cluster import KMeans

# Pre-defined cohort archetypes with standardized profile centroids
# Features: [assessment_pct (0-100), coding_skill (1-3), math_skill (1-3), data_skill (1-3), ml_skill (1-3), streak (1-30)]
COHORT_PROFILES = {
    0: {
        "cohort_name": "Foundational Explorer",
        "description": "Building strong foundational syntax, basic data structures, and mathematical intuition with guided hands-on practice.",
        "pacing": "Structured & Guided",
        "recommended_daily_target_minutes": 45,
        "badge_color": "#3B82F6",
        "learning_strategy": "Focus on bite-sized tutorials, code sandboxes, and foundational quizzes before complex multi-variable models."
    },
    1: {
        "cohort_name": "Algorithmic Builder",
        "description": "Proficient in programming fundamentals; accelerating through statistical modeling, feature engineering, and real-world datasets.",
        "pacing": "Accelerated Applied",
        "recommended_daily_target_minutes": 60,
        "badge_color": "#8B5CF6",
        "learning_strategy": "Emphasize end-to-end dataset wrangling, comparative algorithmic modeling, and Kaggle-style mini-challenges."
    },
    2: {
        "cohort_name": "Advanced AI Practitioner",
        "description": "High domain mastery; tackling deep learning architectures, attention transformers, high-throughput MLOps, and scalable distributed systems.",
        "pacing": "Intensive Deep-Dive",
        "recommended_daily_target_minutes": 90,
        "badge_color": "#10B981",
        "learning_strategy": "Prioritize research paper implementations, custom PyTorch neural modules, hyperparameter tuning, and containerized deployment."
    }
}

class StudentClusterEngine:
    def __init__(self):
        # Synthetic baseline population centroids representing the 3 learner stages
        self.reference_data = np.array([
            [35.0, 1.0, 1.0, 1.0, 1.0, 3.0],   # Beginner Archetype
            [68.0, 2.0, 2.0, 2.0, 1.5, 8.0],   # Intermediate Archetype
            [92.0, 3.0, 3.0, 3.0, 2.8, 15.0]   # Advanced Archetype
        ])
        self.kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.kmeans.fit(self.reference_data)

    def extract_feature_vector(self, assessment_percentage: float, skills_dict: dict, streak_days: int) -> np.ndarray:
        """
        Map qualitative levels (Beginner=1, Intermediate=2, Advanced=3) to numerical vector.
        """
        def level_to_num(lvl):
            if not lvl:
                return 1.0
            l = str(lvl).lower()
            if "adv" in l:
                return 3.0
            if "inter" in l:
                return 2.0
            return 1.0

        coding = level_to_num(skills_dict.get("Python Programming", "Beginner"))
        math = level_to_num(skills_dict.get("Linear Algebra & Calculus", skills_dict.get("Statistics & Probability", "Beginner")))
        data = level_to_num(skills_dict.get("SQL & Databases", skills_dict.get("Data Visualization", "Beginner")))
        ml = level_to_num(skills_dict.get("Machine Learning", "Beginner"))
        streak = min(float(streak_days or 1), 30.0)
        pct = max(0.0, min(100.0, float(assessment_percentage or 50.0)))

        return np.array([[pct, coding, math, data, ml, streak]])

    def assign_cohort(self, assessment_percentage: float, skills_dict: dict, streak_days: int) -> dict:
        """
        Run K-Means inference to predict student's peer cluster and return cohort analytics.
        """
        features = self.extract_feature_vector(assessment_percentage, skills_dict, streak_days)
        cluster_id = int(self.kmeans.predict(features)[0])
        
        # Calculate Euclidean distances to all centroids for confidence metric
        distances = np.linalg.norm(self.kmeans.cluster_centers_ - features, axis=1)
        similarity_score = float(1.0 / (1.0 + distances[cluster_id]))

        cohort_info = COHORT_PROFILES.get(cluster_id, COHORT_PROFILES[0]).copy()
        cohort_info["cluster_id"] = cluster_id
        cohort_info["cluster_similarity"] = round(similarity_score, 3)
        cohort_info["cluster_features"] = {
            "assessment_pct": round(float(features[0][0]), 1),
            "coding_level": float(features[0][1]),
            "math_level": float(features[0][2]),
            "data_level": float(features[0][3]),
            "ml_level": float(features[0][4]),
            "streak_days": int(features[0][5])
        }
        return cohort_info

student_cluster_engine = StudentClusterEngine()
