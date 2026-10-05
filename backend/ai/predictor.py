import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

class PerformancePredictor:
    def __init__(self):
        # Synthetic historical training dataset representing diverse learning trajectories
        # Features: [student_baseline_score (0-100), topic_difficulty (1=Beg, 2=Int, 3=Adv),
        #            prereq_completion_ratio (0.0 - 1.0), time_spent_ratio (0.2 - 2.0)]
        # Target: 1 (Passed quiz on first attempt >= 70%), 0 (Needs reinforcement < 70%)
        X_train = np.array([
            [40, 1, 1.0, 1.0], [50, 1, 1.0, 0.8], [30, 2, 0.5, 0.5], [60, 2, 1.0, 1.0],
            [45, 2, 0.0, 0.5], [75, 2, 1.0, 1.0], [55, 3, 0.5, 0.6], [80, 3, 1.0, 1.2],
            [90, 3, 1.0, 1.0], [35, 1, 0.5, 0.4], [65, 2, 1.0, 0.9], [85, 3, 1.0, 1.5],
            [50, 3, 0.0, 0.4], [70, 1, 1.0, 1.0], [60, 3, 1.0, 1.1], [40, 2, 0.5, 0.7]
        ])
        y_train = np.array([1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0])

        self.model = RandomForestClassifier(n_estimators=20, max_depth=4, random_state=42)
        self.model.fit(X_train, y_train)

        # Decision Tree for interpretable rule explanation
        self.tree_explainer = DecisionTreeClassifier(max_depth=3, random_state=42)
        self.tree_explainer.fit(X_train, y_train)

    def predict_topic_success(self, baseline_score: float, difficulty_str: str, prereq_ratio: float = 1.0, time_ratio: float = 1.0) -> dict:
        diff_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
        diff_val = diff_map.get(str(difficulty_str).lower(), 2)

        features = np.array([[
            max(0.0, min(100.0, float(baseline_score or 50.0))),
            diff_val,
            max(0.0, min(1.0, float(prereq_ratio))),
            max(0.2, min(2.5, float(time_ratio)))
        ]])

        probs = self.model.predict_proba(features)[0]
        pass_prob = float(probs[1]) if len(probs) > 1 else 0.5
        prediction = int(pass_prob >= 0.60)

        # Generate intelligent reasoning
        if pass_prob >= 0.80:
            pacing_advice = "High confidence of mastery. Recommended to advance quickly through practice exercises."
            risk_level = "Low"
        elif pass_prob >= 0.55:
            pacing_advice = "Moderate complexity for your current background. Review key concepts and complete practice problems before the quiz."
            risk_level = "Moderate"
        else:
            pacing_advice = "Challenging advanced material. Strengthen foundational prerequisites and review interactive notes first."
            risk_level = "Elevated"

        return {
            "predicted_pass_probability": round(pass_prob * 100, 1),
            "predicted_pass": bool(prediction),
            "risk_level": risk_level,
            "pacing_advice": pacing_advice,
            "feature_importance": {
                "baseline_mastery": round(float(self.model.feature_importances_[0]), 3),
                "topic_difficulty": round(float(self.model.feature_importances_[1]), 3),
                "prerequisites_cleared": round(float(self.model.feature_importances_[2]), 3),
                "practice_time_investment": round(float(self.model.feature_importances_[3]), 3)
            }
        }

performance_predictor = PerformancePredictor()
