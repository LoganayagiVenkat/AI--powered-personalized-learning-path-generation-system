import json
import logging
from backend.database.db import get_db, init_db, Base, get_engine
from backend.models.models import (
    User, StudentProfile, CareerGoal, Skill, Topic, Subtopic,
    Prerequisite, Assessment, AssessmentQuestion, Quiz, QuizQuestion
)
from werkzeug.security import generate_password_hash

logger = logging.getLogger("learning_path.seed")

def seed_database():
    eng = init_db()
    Base.metadata.create_all(bind=eng)

    db = next(get_db())
    try:
        # Check if already seeded
        if db.query(CareerGoal).first() is not None:
            logger.info("Database already seeded. Ensuring all demo student accounts exist...")
            from backend.database.seed_accounts import seed_demo_accounts
            try:
                seed_demo_accounts()
            except Exception as se:
                logger.warning(f"Demo accounts notice: {se}")
            return

        logger.info("Seeding database with comprehensive career paths, skills, topics, and assessments...")

        # 1. Career Goals
        career_goals = [
            CareerGoal(
                title="Become a Data Scientist",
                target_role="Data Scientist",
                description="Analyze complex data systems, build predictive machine learning models, and uncover actionable business intelligence.",
                required_skills_json=json.dumps([
                    {"skill_name": "Python Programming", "required_level": "Advanced", "weight": 0.25},
                    {"skill_name": "SQL & Databases", "required_level": "Intermediate", "weight": 0.15},
                    {"skill_name": "Statistics & Probability", "required_level": "Advanced", "weight": 0.20},
                    {"skill_name": "Machine Learning", "required_level": "Advanced", "weight": 0.25},
                    {"skill_name": "Data Visualization", "required_level": "Intermediate", "weight": 0.15}
                ])
            ),
            CareerGoal(
                title="Become an AI / Machine Learning Engineer",
                target_role="AI / ML Engineer",
                description="Design, optimize, and deploy production-grade deep learning, computer vision, and NLP architectures at scale.",
                required_skills_json=json.dumps([
                    {"skill_name": "Python Programming", "required_level": "Advanced", "weight": 0.20},
                    {"skill_name": "Linear Algebra & Calculus", "required_level": "Intermediate", "weight": 0.15},
                    {"skill_name": "Machine Learning", "required_level": "Advanced", "weight": 0.25},
                    {"skill_name": "Deep Learning & Neural Networks", "required_level": "Advanced", "weight": 0.25},
                    {"skill_name": "Natural Language Processing (NLP)", "required_level": "Intermediate", "weight": 0.15}
                ])
            ),
            CareerGoal(
                title="Become a Full Stack Software Engineer",
                target_role="Full Stack Developer",
                description="Develop scalable end-to-end web applications with modern frontend frameworks and robust backend microservices.",
                required_skills_json=json.dumps([
                    {"skill_name": "Python Programming", "required_level": "Intermediate", "weight": 0.20},
                    {"skill_name": "JavaScript & React", "required_level": "Advanced", "weight": 0.30},
                    {"skill_name": "SQL & Databases", "required_level": "Intermediate", "weight": 0.20},
                    {"skill_name": "REST API Architecture", "required_level": "Advanced", "weight": 0.20},
                    {"skill_name": "Git & DevOps Basics", "required_level": "Intermediate", "weight": 0.10}
                ])
            )
        ]
        db.add_all(career_goals)
        db.commit()

        # 2. Skills
        skills = [
            Skill(name="Python Programming", category="Programming", description="Core language fundamentals, data structures, list comprehensions, and idiomatic Python."),
            Skill(name="SQL & Databases", category="Data", description="Relational schema design, normalization, complex multi-table joins, indexing, and aggregations."),
            Skill(name="Statistics & Probability", category="Mathematics", description="Hypothesis testing, distributions, Bayes theorem, p-values, variance, and standard deviation."),
            Skill(name="Linear Algebra & Calculus", category="Mathematics", description="Vectors, matrix operations, eigenvalues, eigenvectors, gradients, and partial derivatives."),
            Skill(name="Data Visualization", category="Data", description="Storytelling with data using Matplotlib, Seaborn, interactive Plotly charts, and dashboarding."),
            Skill(name="Machine Learning", category="AI/ML", description="Supervised/unsupervised algorithms, regularization, decision trees, cross-validation, and metrics."),
            Skill(name="Deep Learning & Neural Networks", category="AI/ML", description="Backpropagation, perceptrons, CNNs, RNNs, PyTorch/TensorFlow, and attention mechanisms."),
            Skill(name="Natural Language Processing (NLP)", category="AI/ML", description="Text tokenization, TF-IDF, embeddings, sentiment analysis, and transformer models."),
            Skill(name="JavaScript & React", category="Web", description="Modern ES6+, component lifecycle, hooks, state management, and DOM optimization."),
            Skill(name="REST API Architecture", category="Web", description="HTTP protocols, stateless request design, JSON serialization, auth tokens, and status codes.")
        ]
        db.add_all(skills)
        db.commit()

        # 3. Topics with rich descriptions, key concepts, resources, practice exercises
        topics_data = [
            {
                "title": "Python Programming Fundamentals",
                "category": "Programming",
                "difficulty": "Beginner",
                "estimated_hours": 6,
                "description": "Master Python syntax, control flow, functions, dictionaries, file I/O, and error handling for data and software applications.",
                "concepts": ["Variables & Data Types", "Conditionals & Loops", "Functions & Scope", "List Comprehensions", "File Operations"],
                "resources": [
                    {"title": "Official Python Tutorial", "type": "Documentation", "url": "https://docs.python.org/3/tutorial/"},
                    {"title": "Python for Everybody", "type": "Course", "url": "https://www.py4e.com/"},
                    {"title": "Automate the Boring Stuff with Python", "type": "Book", "url": "https://automatetheboringstuff.com/"}
                ],
                "exercises": [
                    "Implement a word frequency counter reading from a raw text file.",
                    "Build a JSON parser script that filters and aggregates user records.",
                    "Write a prime number generator using efficient list comprehension."
                ],
                "subtopics": [
                    ("Python Syntax & Data Structures", "Deep dive into lists, tuples, dictionaries, and sets with time complexities.", "Detailed guide on Python data structures, memory references, and mutability."),
                    ("Functions & Modular Code", "Learn how to write clean, reusable, decoupled functions and modules.", "Covers argument unpacking (*args, **kwargs), lambda expressions, and decorators."),
                    ("Exception Handling & File I/O", "Safely read, write, and process external files while handling runtime errors.", "Using with statements, custom exceptions, and structured JSON parsing.")
                ]
            },
            {
                "title": "Advanced Python & Object-Oriented Design",
                "category": "Programming",
                "difficulty": "Intermediate",
                "estimated_hours": 8,
                "description": "Construct robust object-oriented software architectures, classes, inheritance, dunder methods, and generator pipelines.",
                "concepts": ["Classes & Objects", "Inheritance & Polymorphism", "Dunder Methods (__init__, __repr__)", "Generators & Iterators", "Decorators"],
                "resources": [
                    {"title": "Fluent Python (Luciano Ramalho)", "type": "Book", "url": "https://www.oreilly.com/library/view/fluent-python/9781491946237/"},
                    {"title": "Real Python OOP Guide", "type": "Tutorial", "url": "https://realpython.com/python3-object-oriented-programming/"}
                ],
                "exercises": [
                    "Design a bank account simulation class hierarchy with transaction history logging.",
                    "Create a custom iterator that streams lines from large multi-gigabyte dataset files.",
                    "Write an execution timing decorator to measure function performance."
                ],
                "subtopics": [
                    ("OOP Core Principles", "Encapsulation, inheritance, and polymorphism in Python.", "Building modular domain models with clean class interfaces."),
                    ("Generators and Memory Optimization", "Processing massive datasets without exhausting RAM using yield.", "Building lazy evaluation pipelines and custom iterators.")
                ]
            },
            {
                "title": "SQL & Relational Database Engineering",
                "category": "Data",
                "difficulty": "Intermediate",
                "estimated_hours": 7,
                "description": "Query relational databases with SQL: filtering, grouping, window functions, table joins, transactions, and indexing.",
                "concepts": ["SELECT & Filtering", "INNER/LEFT/RIGHT JOINs", "GROUP BY & Aggregations", "Subqueries & CTEs", "Window Functions"],
                "resources": [
                    {"title": "SQLZoo Interactive Exercises", "type": "Practice", "url": "https://sqlzoo.net/"},
                    {"title": "Mode Analytics SQL Tutorial", "type": "Guide", "url": "https://mode.com/sql-tutorial/"}
                ],
                "exercises": [
                    "Write a multi-table JOIN query to calculate monthly customer retention rates.",
                    "Use window functions (ROW_NUMBER, RANK) to identify top 3 earners per department.",
                    "Optimize a slow query using EXPLAIN plan and adding covering indexes."
                ],
                "subtopics": [
                    ("Relational Foundations & Joins", "Connecting disparate tables using primary and foreign keys.", "Deep dive into INNER, LEFT, FULL OUTER joins with cardinality."),
                    ("Aggregation, Grouping & Window Functions", "Summarizing business metrics with GROUP BY and analytical window functions.", "PARTITION BY, ORDER BY, and rolling averages.")
                ]
            },
            {
                "title": "Mathematics & Linear Algebra for AI",
                "category": "Mathematics",
                "difficulty": "Intermediate",
                "estimated_hours": 9,
                "description": "Essential mathematical foundations: matrix multiplications, vectors, dot products, eigenvalues, and gradient calculus.",
                "concepts": ["Vector Spaces", "Matrix Operations & Inversion", "Eigenvalues & Eigenvectors", "Dot Products & Projections", "Partial Derivatives"],
                "resources": [
                    {"title": "3Blue1Brown: Essence of Linear Algebra", "type": "Video Series", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"},
                    {"title": "Mathematics for Machine Learning (Deisenroth)", "type": "Book", "url": "https://mml-book.github.io/"}
                ],
                "exercises": [
                    "Implement 2D and 3D matrix transformation and rotation from scratch using NumPy.",
                    "Calculate eigenvalues and eigenvectors for a covariance matrix.",
                    "Compute analytical partial derivatives for a multivariate loss function."
                ],
                "subtopics": [
                    ("Vectors & Matrix Transformations", "Geometric intuition behind linear mappings and coordinate transformations.", "Dot products, orthogonal projections, and basis vectors."),
                    ("Matrix Decomposition & Eigenvalues", "Dimensionality reduction intuition through PCA and spectral decomposition.", "Eigenvectors as principal axes of variance.")
                ]
            },
            {
                "title": "Probability & Descriptive Statistics",
                "category": "Mathematics",
                "difficulty": "Intermediate",
                "estimated_hours": 8,
                "description": "Descriptive statistics, normal/binomial distributions, central limit theorem, hypothesis testing, and p-value inference.",
                "concepts": ["Mean, Median, Standard Deviation", "Probability Distributions", "Central Limit Theorem", "Hypothesis Testing (A/B Testing)", "Bayes' Theorem"],
                "resources": [
                    {"title": "StatQuest with Josh Starmer", "type": "Video Series", "url": "https://statquest.org/"},
                    {"title": "Think Stats (Allen B. Downey)", "type": "Book", "url": "https://greenteapress.com/wp/think-stats-2e/"}
                ],
                "exercises": [
                    "Conduct a two-sample t-test to evaluate conversion rates in an A/B test.",
                    "Simulate 10,000 coin flips and prove the Central Limit Theorem visually.",
                    "Calculate posterior probabilities using Bayes theorem for diagnostic tests."
                ],
                "subtopics": [
                    ("Distributions & Central Limit Theorem", "Normal, Poisson, and Bernoulli distributions with variance.", "Why sample means converge to normal distribution."),
                    ("Statistical Inference & Hypothesis Testing", "Null hypothesis, significance alpha, p-values, and Type I/II errors.", "Practical interpretation of statistical significance in industry.")
                ]
            },
            {
                "title": "Exploratory Data Analysis & Visualization",
                "category": "Data",
                "difficulty": "Intermediate",
                "estimated_hours": 6,
                "description": "Transform messy raw datasets with Pandas, handle missing values, detect outliers, and build insightful visual plots.",
                "concepts": ["Pandas DataFrames", "Data Cleaning & Imputation", "Feature Distributions", "Correlation Heatmaps", "Plotly & Seaborn"],
                "resources": [
                    {"title": "Python Data Science Handbook", "type": "Book", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/"},
                    {"title": "Kaggle EDA Micro-Course", "type": "Interactive", "url": "https://www.kaggle.com/learn/data-visualization"}
                ],
                "exercises": [
                    "Clean a real-world messy CSV dataset with missing fields and erroneous data types.",
                    "Produce an interactive multi-dimensional scatter plot highlighting clustered segments.",
                    "Generate a correlation matrix and identify multicollinearity among features."
                ],
                "subtopics": [
                    ("Data Wrangling with Pandas", "Filtering, grouping, merging, and reshaping tabular datasets.", "Handling nulls, datetime transformations, and categorical encoding."),
                    ("Data Visualization & Visual Storytelling", "Choosing the right plot type: histograms, box plots, scatter, heatmaps.", "Building informative dashboards and aesthetic charts.")
                ]
            },
            {
                "title": "Supervised Machine Learning Algorithms",
                "category": "AI/ML",
                "difficulty": "Intermediate",
                "estimated_hours": 10,
                "description": "Core predictive modeling: Linear Regression, Logistic Regression, Decision Trees, Random Forests, and Gradient Boosting.",
                "concepts": ["Regression vs Classification", "Loss Functions & Cost Minimization", "Bias-Variance Tradeoff", "Overfitting & Regularization (L1/L2)", "Ensemble Methods"],
                "resources": [
                    {"title": "Scikit-Learn Official User Guide", "type": "Documentation", "url": "https://scikit-learn.org/stable/user_guide.html"},
                    {"title": "Coursera: Machine Learning Specialization", "type": "Course", "url": "https://www.coursera.org/specializations/machine-learning-introduction"}
                ],
                "exercises": [
                    "Train a Random Forest classifier on customer churn data and evaluate ROC-AUC.",
                    "Implement Linear Regression with Gradient Descent from scratch in Python.",
                    "Tune hyperparameters of an XGBoost model using GridSearchCV."
                ],
                "subtopics": [
                    ("Linear Models & Regularization", "Linear and logistic regression with Ridge and Lasso penalties.", "Mathematical formulation of loss minimization and gradient descent."),
                    ("Tree-Based Models & Ensembles", "Decision trees, Random Forests, and Gradient Boosted Trees.", "Bagging, boosting, feature importance, and handling non-linear relationships.")
                ]
            },
            {
                "title": "Unsupervised ML & Clustering",
                "category": "AI/ML",
                "difficulty": "Intermediate",
                "estimated_hours": 7,
                "description": "Discover latent structures: K-Means clustering, Hierarchical clustering, PCA dimensionality reduction, and anomaly detection.",
                "concepts": ["K-Means Algorithm", "Elbow Method & Silhouette Score", "Hierarchical Clustering & Dendrograms", "PCA (Principal Component Analysis)", "Anomaly Detection"],
                "resources": [
                    {"title": "Hands-On Machine Learning (Aurélien Géron)", "type": "Book", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/"},
                    {"title": "Clustering Algorithms in Scikit-Learn", "type": "Tutorial", "url": "https://scikit-learn.org/stable/modules/clustering.html"}
                ],
                "exercises": [
                    "Segment e-commerce customers into behavioral clusters using K-Means and PCA.",
                    "Determine optimal cluster count K using inertia plots and silhouette analysis.",
                    "Detect fraudulent transactions using Isolation Forest anomaly detection."
                ],
                "subtopics": [
                    ("Partitioning & K-Means Clustering", "Iterative centroid assignment and convergence criteria.", "Choosing K and diagnosing cluster separation quality."),
                    ("Dimensionality Reduction with PCA", "Projecting high-dimensional feature spaces onto orthogonal principal axes.", "Preserving variance while drastically reducing computational overhead.")
                ]
            },
            {
                "title": "Deep Learning & Neural Networks",
                "category": "AI/ML",
                "difficulty": "Advanced",
                "estimated_hours": 12,
                "description": "Artificial neural networks, backpropagation, activation functions, convolutional neural networks (CNNs), and PyTorch frameworks.",
                "concepts": ["Multi-Layer Perceptrons (MLP)", "Backpropagation & Chain Rule", "Activation Functions (ReLU, Softmax)", "CNNs for Computer Vision", "PyTorch Tensors & Training Loops"],
                "resources": [
                    {"title": "Deep Learning with Python (François Chollet)", "type": "Book", "url": "https://www.manning.com/books/deep-learning-with-python"},
                    {"title": "DeepLearning.AI: Deep Learning Specialization", "type": "Course", "url": "https://www.deeplearning.ai/courses/deep-learning-specialization/"}
                ],
                "exercises": [
                    "Build a multi-layer neural network from scratch using NumPy with manual backprop.",
                    "Train a CNN in PyTorch to classify handwritten digits with >98% accuracy.",
                    "Implement learning rate scheduling and early stopping callbacks."
                ],
                "subtopics": [
                    ("Neural Network Foundations & Backprop", "Forward pass, loss calculation, chain rule gradients, weight updates.", "Understanding vanishing gradients and modern optimizers (Adam, RMSprop)."),
                    ("Convolutional Architectures & Vision", "Kernels, feature maps, pooling layers, and transfer learning.", "Fine-tuning pre-trained models for image classification.")
                ]
            },
            {
                "title": "Natural Language Processing (NLP) & Transformers",
                "category": "AI/ML",
                "difficulty": "Advanced",
                "estimated_hours": 11,
                "description": "Tokenization, TF-IDF vectorization, Word2Vec embeddings, sequence modeling, attention mechanisms, and Transformer architectures.",
                "concepts": ["Tokenization & Stopword Filtering", "TF-IDF Vector Space Models", "Word & Sentence Embeddings", "Self-Attention Mechanism", "Transformer Architectures (BERT, GPT)"],
                "resources": [
                    {"title": "Hugging Face NLP Course", "type": "Course", "url": "https://huggingface.co/learn/nlp-course"},
                    {"title": "Speech and Language Processing (Jurafsky & Martin)", "type": "Book", "url": "https://web.stanford.edu/~jurafsky/slp3/"}
                ],
                "exercises": [
                    "Build a document similarity search engine using TF-IDF and Cosine Similarity.",
                    "Fine-tune a BERT model for multi-class intent classification.",
                    "Implement a text generation prompt pipeline with temperature sampling."
                ],
                "subtopics": [
                    ("Text Preprocessing & Vectorization", "Bag-of-Words, TF-IDF weighting, n-grams, and semantic dense embeddings.", "Measuring document distances using cosine metrics."),
                    ("Attention Mechanisms & Modern LLMs", "Query, Key, Value attention formulation and multi-head self-attention.", "How modern transformers process contextual sequences in parallel.")
                ]
            },
            {
                "title": "MLOps, Model Deployment & System Evaluation",
                "category": "AI/ML",
                "difficulty": "Advanced",
                "estimated_hours": 8,
                "description": "Productionize machine learning models: REST API serving with FastAPI/Flask, Docker containerization, monitoring, and data drift detection.",
                "concepts": ["Model Serialization (Pickle/ONNX)", "REST API Endpoints for Inference", "Docker Containers", "Data Drift & Concept Drift", "CI/CD Pipelines for ML"],
                "resources": [
                    {"title": "Made With ML (Goku Mohandas)", "type": "Course", "url": "https://madewithml.com/"},
                    {"title": "Full Stack Deep Learning", "type": "Course", "url": "https://fullstackdeeplearning.com/"}
                ],
                "exercises": [
                    "Wrap a scikit-learn model inside a high-performance REST API with input validation.",
                    "Containerize the inference API with Docker and test latency under load.",
                    "Set up automated logging to track inference distribution drift over time."
                ],
                "subtopics": [
                    ("Model Serving & Low-Latency APIs", "Building scalable RESTful endpoints for real-time predictions.", "Batch inference vs real-time low-latency request handling."),
                    ("Monitoring & Drift Detection", "Detecting degradation in live prediction accuracy when data distributions shift.", "Retraining triggers, model versioning, and canary deployments.")
                ]
            },
            {
                "title": "Capstone Data Science & AI Project",
                "category": "AI/ML",
                "difficulty": "Advanced",
                "estimated_hours": 14,
                "description": "Synthesize all acquired skills into an end-to-end production AI pipeline: data ingestion, EDA, modeling, web dashboard, and API serving.",
                "concepts": ["End-to-End Pipeline Architecture", "Model Validation & Stress Testing", "Interactive Web UI", "Production Documentation"],
                "resources": [
                    {"title": "Data Science Portfolio Project Guide", "type": "Guide", "url": "https://towardsdatascience.com/how-to-build-a-data-science-portfolio-5f5660249492"}
                ],
                "exercises": [
                    "Formulate a complete real-world problem statement and collect datasets.",
                    "Train baseline and advanced models with rigorous ablation studies.",
                    "Deploy the complete interactive application with documentation and performance reports."
                ],
                "subtopics": [
                    ("System Architecture & Data Pipeline", "Designing the full lifecycle from raw data ingestion to database storage.", "Ensuring reproducible experiment tracking."),
                    ("Production Launch & Presentation", "Writing executive summaries, technical documentation, and interactive demos.", "Showcasing business impact and algorithmic decisions.")
                ]
            }
        ]

        created_topics = {}
        for t_info in topics_data:
            topic = Topic(
                title=t_info["title"],
                category=t_info["category"],
                difficulty=t_info["difficulty"],
                estimated_hours=t_info["estimated_hours"],
                description=t_info["description"],
                key_concepts_json=json.dumps(t_info["concepts"]),
                resources_json=json.dumps(t_info["resources"]),
                practice_exercises_json=json.dumps(t_info["exercises"])
            )
            db.add(topic)
            db.flush()
            created_topics[topic.title] = topic

            for idx, (st_title, st_summary, st_content) in enumerate(t_info["subtopics"], 1):
                subtopic = Subtopic(
                    topic_id=topic.id,
                    title=st_title,
                    order_index=idx,
                    summary=st_summary,
                    learning_content=st_content
                )
                db.add(subtopic)

        db.commit()

        # 4. Prerequisites (Directed Acyclic Graph)
        prereqs = [
            ("Advanced Python & Object-Oriented Design", "Python Programming Fundamentals"),
            ("SQL & Relational Database Engineering", "Python Programming Fundamentals"),
            ("Mathematics & Linear Algebra for AI", "Python Programming Fundamentals"),
            ("Probability & Descriptive Statistics", "Mathematics & Linear Algebra for AI"),
            ("Exploratory Data Analysis & Visualization", "Python Programming Fundamentals"),
            ("Exploratory Data Analysis & Visualization", "SQL & Relational Database Engineering"),
            ("Supervised Machine Learning Algorithms", "Probability & Descriptive Statistics"),
            ("Supervised Machine Learning Algorithms", "Advanced Python & Object-Oriented Design"),
            ("Unsupervised ML & Clustering", "Supervised Machine Learning Algorithms"),
            ("Deep Learning & Neural Networks", "Supervised Machine Learning Algorithms"),
            ("Deep Learning & Neural Networks", "Mathematics & Linear Algebra for AI"),
            ("Natural Language Processing (NLP) & Transformers", "Deep Learning & Neural Networks"),
            ("MLOps, Model Deployment & System Evaluation", "Supervised Machine Learning Algorithms"),
            ("MLOps, Model Deployment & System Evaluation", "SQL & Relational Database Engineering"),
            ("Capstone Data Science & AI Project", "Deep Learning & Neural Networks"),
            ("Capstone Data Science & AI Project", "MLOps, Model Deployment & System Evaluation")
        ]

        for topic_title, prereq_title in prereqs:
            if topic_title in created_topics and prereq_title in created_topics:
                db.add(Prerequisite(
                    topic_id=created_topics[topic_title].id,
                    prerequisite_topic_id=created_topics[prereq_title].id
                ))
        db.commit()

        # 5. Diagnostic Skill Assessment & Questions
        diag_assessment = Assessment(
            title="Comprehensive Technical Skill Assessment",
            category="Diagnostics",
            description="Evaluate your current knowledge across Python, Mathematics, SQL, Statistics, and Machine Learning to establish your personalized baseline.",
            total_questions=10,
            time_limit_minutes=15
        )
        db.add(diag_assessment)
        db.flush()

        assessment_q_data = [
            {
                "topic": "Python Programming Fundamentals",
                "question": "In Python, what is the output of `type([]) == list` and how are lists represented in memory?",
                "options": ["True; dynamic contiguous array of pointers", "False; linked list", "True; hash map", "False; fixed-size buffer"],
                "answer": "True; dynamic contiguous array of pointers",
                "difficulty": "Beginner",
                "explanation": "Python lists are implemented under the hood as dynamically-sized arrays of object references (pointers)."
            },
            {
                "topic": "Python Programming Fundamentals",
                "question": "Which Python construct allows functions to yield values one at a time without loading the entire sequence into memory?",
                "options": ["Decorators", "Generators using `yield`", "Context Managers", "Metaclasses"],
                "answer": "Generators using `yield`",
                "difficulty": "Intermediate",
                "explanation": "Generators use the `yield` keyword to implement iterator protocol with lazy evaluation, conserving memory."
            },
            {
                "topic": "SQL & Relational Database Engineering",
                "question": "Which SQL clause is used to filter groups created by a `GROUP BY` statement rather than individual rows?",
                "options": ["WHERE", "HAVING", "ORDER BY", "QUALIFY"],
                "answer": "HAVING",
                "difficulty": "Beginner",
                "explanation": "WHERE filters rows before aggregation, whereas HAVING filters grouped aggregated records."
            },
            {
                "topic": "SQL & Relational Database Engineering",
                "question": "What is the primary difference between `RANK()` and `DENSE_RANK()` in SQL window functions?",
                "options": ["RANK leaves gaps in rankings after ties; DENSE_RANK does not", "DENSE_RANK orders descending by default", "RANK cannot be partitioned", "There is no difference"],
                "answer": "RANK leaves gaps in rankings after ties; DENSE_RANK does not",
                "difficulty": "Intermediate",
                "explanation": "If two rows tie for 1st place, RANK assigns 1, 1, 3. DENSE_RANK assigns 1, 1, 2."
            },
            {
                "topic": "Mathematics & Linear Algebra for AI",
                "question": "If the dot product between two non-zero vectors equals zero, what does this indicate geometrically?",
                "options": ["The vectors are parallel", "The vectors are orthogonal (perpendicular)", "The vectors have identical magnitude", "The vectors are linearly dependent"],
                "answer": "The vectors are orthogonal (perpendicular)",
                "difficulty": "Intermediate",
                "explanation": "The dot product is |A||B|cos(θ). When θ = 90°, cos(θ) = 0, indicating orthogonal vectors."
            },
            {
                "topic": "Probability & Descriptive Statistics",
                "question": "What does a p-value of 0.03 indicate when testing a null hypothesis at an alpha level of 0.05?",
                "options": ["The null hypothesis has a 97% probability of being true", "Reject the null hypothesis as the result is statistically significant", "Fail to reject the null hypothesis", "The experiment had a 3% measurement error"],
                "answer": "Reject the null hypothesis as the result is statistically significant",
                "difficulty": "Intermediate",
                "explanation": "When p-value < alpha (0.03 < 0.05), we reject the null hypothesis in favor of the alternative hypothesis."
            },
            {
                "topic": "Supervised Machine Learning Algorithms",
                "question": "What problem does L2 regularization (Ridge) primarily mitigate in linear regression?",
                "options": ["Underfitting due to low model capacity", "Overfitting by penalizing large model coefficients", "Slow gradient descent convergence", "Missing categorical features"],
                "answer": "Overfitting by penalizing large model coefficients",
                "difficulty": "Intermediate",
                "explanation": "L2 regularization adds a squared magnitude penalty to the loss function, shrinking weights and preventing overfitting."
            },
            {
                "topic": "Supervised Machine Learning Algorithms",
                "question": "In classification problems with severe class imbalance (e.g. 99% negative, 1% positive), which metric is LEAST informative?",
                "options": ["Precision", "Recall", "ROC-AUC", "Raw Accuracy"],
                "answer": "Raw Accuracy",
                "difficulty": "Intermediate",
                "explanation": "A dummy classifier predicting all negatives achieves 99% accuracy while finding zero positive instances."
            },
            {
                "topic": "Unsupervised ML & Clustering",
                "question": "Which heuristic method is commonly used to find the optimal number of clusters K in K-Means?",
                "options": ["Backpropagation", "Elbow method analyzing Inertia/Within-Cluster Sum of Squares", "Cross-validation log loss", "Fourier Transform"],
                "answer": "Elbow method analyzing Inertia/Within-Cluster Sum of Squares",
                "difficulty": "Intermediate",
                "explanation": "The elbow method plots inertia vs K to locate the point of diminishing returns where inertia decline flattens."
            },
            {
                "topic": "Natural Language Processing (NLP) & Transformers",
                "question": "What does the 'TF' in TF-IDF represent and how does it balance against 'IDF'?",
                "options": ["Term Frequency; it measures word prevalence in a document while IDF discounts words common across all documents", "Text Form; it standardizes casing", "Total Features; it counts total vocabulary size", "Training Factor; it scales gradients"],
                "answer": "Term Frequency; it measures word prevalence in a document while IDF discounts words common across all documents",
                "difficulty": "Intermediate",
                "explanation": "TF rewards frequent occurrences within a text, while IDF penalizes stop words appearing universally across the entire corpus."
            }
        ]

        for q in assessment_q_data:
            t_obj = created_topics.get(q["topic"])
            db.add(AssessmentQuestion(
                assessment_id=diag_assessment.id,
                topic_id=t_obj.id if t_obj else None,
                question_text=q["question"],
                options_json=json.dumps(q["options"]),
                correct_answer=q["answer"],
                difficulty=q["difficulty"],
                explanation=q["explanation"]
            ))
        db.commit()

        # 6. Topic Quizzes
        for t_title, t_obj in created_topics.items():
            quiz = Quiz(
                topic_id=t_obj.id,
                title=f"{t_title} Mastery Quiz",
                difficulty=t_obj.difficulty,
                time_limit_minutes=10
            )
            db.add(quiz)
            db.flush()

            # Add 3 questions per quiz
            db.add_all([
                QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=f"What is the foundational concept behind {t_title}?",
                    options_json=json.dumps([
                        f"Structured mathematical and algorithmic paradigms in {t_obj.category}",
                        "Static hardcoded decision trees without updates",
                        "Manual execution of repetitive loops",
                        "Ignoring data types and constraints"
                    ]),
                    correct_answer=f"Structured mathematical and algorithmic paradigms in {t_obj.category}",
                    explanation=f"Understanding foundational principles in {t_obj.category} is critical for real-world mastery."
                ),
                QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=f"Which real-world scenario directly relies on {t_title}?",
                    options_json=json.dumps([
                        "Building predictive pipelines, processing real-world data, and automating intelligent decisions",
                        "Only decorative CSS styling",
                        "Restarting physical computer hardware",
                        "Printing text to terminal without logic"
                    ]),
                    correct_answer="Building predictive pipelines, processing real-world data, and automating intelligent decisions",
                    explanation=f"{t_title} is actively applied across industry engineering and data workflows."
                ),
                QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=f"When encountering edge cases in {t_title}, what is the best practice?",
                    options_json=json.dumps([
                        "Thorough validation, error handling, performance metrics, and testing assumptions",
                        "Ignoring errors and continuing execution",
                        "Deleting the test cases",
                        "Hardcoding all expected outputs"
                    ]),
                    correct_answer="Thorough validation, error handling, performance metrics, and testing assumptions",
                    explanation="Production software and models require systematic testing and metric monitoring."
                )
            ])

        db.commit()

        # 7. Demo Student User for Instant Testing
        demo_user = User(
            name="Alex Morgan",
            email="alex.morgan@example.com",
            password_hash=generate_password_hash("password123")
        )
        db.add(demo_user)
        db.flush()

        data_science_goal = career_goals[0]
        demo_profile = StudentProfile(
            user_id=demo_user.id,
            education_level="Undergraduate",
            experience_level="Beginner",
            interests="Machine Learning, Data Science, Python, Predictive Analytics, AI",
            career_goal_id=data_science_goal.id,
            target_job_role="Data Scientist",
            overall_skill_level="Beginner",
            bio="Aspiring Data Scientist with basic Python and Math foundations looking to master Machine Learning and modern AI pipelines.",
            streak_days=4,
            total_learning_minutes=180
        )
        db.add(demo_profile)
        db.commit()

        logger.info("Database seeding successfully completed!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during database seed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
