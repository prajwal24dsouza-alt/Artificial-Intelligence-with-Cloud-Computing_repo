"""
Assignment: ML Idea Generator
Description: Suggest ML problems in College, Healthcare, and Shopping domains
              and describe Input → Output for each problem.
"""

import random
from textwrap import dedent

# ──────────────────────────────────────────────
#  ML Problem Ideas Database
# ──────────────────────────────────────────────

ml_ideas = {

    # ═══════════════════════════════════════════
    #  COLLEGE DOMAIN
    # ═══════════════════════════════════════════
    "College": [
        {
            "title": "Student Dropout Prediction",
            "description": (
                "Predict whether a student is likely to drop out of college "
                "based on academic performance, attendance, financial status, "
                "and engagement metrics."
            ),
            "ml_type": "Supervised – Binary Classification",
            "input": [
                "Attendance percentage",
                "GPA / semester grades",
                "Family income level",
                "Participation in extracurricular activities",
                "Number of backlogs / failed subjects",
            ],
            "output": "Dropout Risk Label  →  'High Risk' or 'Low Risk'  (0 / 1)",
            "algorithm": "Logistic Regression, Random Forest, XGBoost",
        },
        {
            "title": "Student Grade Prediction",
            "description": (
                "Predict the final grade of a student based on their study "
                "habits, past performance, and class participation."
            ),
            "ml_type": "Supervised – Regression",
            "input": [
                "Hours studied per week",
                "Past semester GPA",
                "Assignment completion rate",
                "Class attendance percentage",
                "Online resource usage hours",
            ],
            "output": "Predicted Final Grade  →  Numeric score (e.g., 0–100 or GPA scale)",
            "algorithm": "Linear Regression, Decision Tree Regressor, SVR",
        },
        {
            "title": "Course Recommendation System",
            "description": (
                "Recommend elective courses to students based on their past "
                "course preferences, grades, and career interests."
            ),
            "ml_type": "Unsupervised / Collaborative Filtering",
            "input": [
                "List of completed courses with grades",
                "Student's department / major",
                "Career interest keywords",
                "Peer enrollment patterns",
                "Course difficulty ratings",
            ],
            "output": "Top-N Recommended Elective Courses  →  Ranked list of course names",
            "algorithm": "K-Nearest Neighbors, Matrix Factorization, Content-Based Filtering",
        },
        {
            "title": "Campus Placement Prediction",
            "description": (
                "Predict whether a student will be placed in campus recruitment "
                "and estimate the expected salary package."
            ),
            "ml_type": "Supervised – Classification + Regression",
            "input": [
                "CGPA",
                "Number of internships completed",
                "Technical skills score",
                "Communication skills rating",
                "Number of projects / certifications",
            ],
            "output": "Placement Status ('Placed' / 'Not Placed')  +  Expected Salary (₹ LPA)",
            "algorithm": "Random Forest, Gradient Boosting, Neural Network",
        },
        {
            "title": "Student Engagement Analysis",
            "description": (
                "Analyze student engagement in online classes by processing "
                "webcam feeds and interaction logs to detect attentiveness."
            ),
            "ml_type": "Supervised – Image Classification + NLP",
            "input": [
                "Webcam image frames (face orientation, eye gaze)",
                "Chat / Q&A participation count",
                "Quiz response time",
                "Screen-on duration vs class duration",
                "Mouse / keyboard activity logs",
            ],
            "output": "Engagement Level  →  'Highly Engaged', 'Moderate', 'Disengaged'",
            "algorithm": "CNN (for images), LSTM, Ensemble Methods",
        },
    ],

    # ═══════════════════════════════════════════
    #  HEALTHCARE DOMAIN
    # ═══════════════════════════════════════════
    "Healthcare": [
        {
            "title": "Disease Prediction from Symptoms",
            "description": (
                "Predict the most probable disease a patient might have based "
                "on the symptoms they report."
            ),
            "ml_type": "Supervised – Multi-class Classification",
            "input": [
                "List of symptoms (fever, cough, headache, etc.)",
                "Patient age and gender",
                "Duration of symptoms (days)",
                "Pre-existing conditions",
                "Family medical history flags",
            ],
            "output": "Predicted Disease Name  →  e.g., 'Flu', 'Diabetes', 'Malaria'",
            "algorithm": "Naïve Bayes, Decision Tree, Random Forest",
        },
        {
            "title": "Heart Disease Risk Assessment",
            "description": (
                "Assess a patient's risk of developing heart disease using "
                "clinical measurements and lifestyle data."
            ),
            "ml_type": "Supervised – Binary Classification",
            "input": [
                "Age, gender, BMI",
                "Blood pressure (systolic / diastolic)",
                "Cholesterol level (mg/dL)",
                "Smoking status (Yes / No)",
                "Resting ECG results",
            ],
            "output": "Heart Disease Risk  →  'Positive' or 'Negative'  (1 / 0)",
            "algorithm": "Logistic Regression, SVM, XGBoost",
        },
        {
            "title": "Medical Image Diagnosis (X-Ray / MRI)",
            "description": (
                "Automatically detect abnormalities such as pneumonia, tumors, "
                "or fractures from medical imaging data."
            ),
            "ml_type": "Supervised – Image Classification",
            "input": [
                "X-Ray / MRI scan image (pixel data)",
                "Patient age and gender",
                "Body part being scanned",
                "Image resolution and contrast settings",
                "Previous scan history (if available)",
            ],
            "output": "Diagnosis Label  →  'Normal' / 'Pneumonia' / 'Tumor Detected'  + Confidence %",
            "algorithm": "Convolutional Neural Networks (CNN), ResNet, VGG-16",
        },
        {
            "title": "Patient Readmission Prediction",
            "description": (
                "Predict the likelihood that a discharged patient will be "
                "readmitted to the hospital within 30 days."
            ),
            "ml_type": "Supervised – Binary Classification",
            "input": [
                "Length of previous hospital stay (days)",
                "Number of past admissions",
                "Discharge diagnosis code",
                "Medication count at discharge",
                "Follow-up appointment scheduled (Yes / No)",
            ],
            "output": "Readmission Prediction  →  'Will be Readmitted' / 'Not Readmitted'",
            "algorithm": "Gradient Boosting, Random Forest, Logistic Regression",
        },
        {
            "title": "Drug Dosage Optimization",
            "description": (
                "Recommend the optimal drug dosage for a patient based on "
                "their body metrics, medical history, and drug interactions."
            ),
            "ml_type": "Supervised – Regression",
            "input": [
                "Patient weight and height",
                "Age and kidney/liver function indicators",
                "Current medications list",
                "Genetic markers (pharmacogenomics data)",
                "Target drug name",
            ],
            "output": "Recommended Dosage  →  Numeric value in mg (e.g., 250 mg twice daily)",
            "algorithm": "Linear Regression, Neural Network, Reinforcement Learning",
        },
    ],

    # ═══════════════════════════════════════════
    #  SHOPPING DOMAIN
    # ═══════════════════════════════════════════
    "Shopping": [
        {
            "title": "Product Recommendation Engine",
            "description": (
                "Recommend products to customers based on their browsing "
                "history, past purchases, and similar user preferences."
            ),
            "ml_type": "Collaborative Filtering / Content-Based",
            "input": [
                "User browsing history (product IDs viewed)",
                "Past purchase history",
                "Product ratings given by the user",
                "User demographic info (age, location)",
                "Current cart contents",
            ],
            "output": "Top-N Recommended Products  →  Ranked list of Product IDs / Names",
            "algorithm": "K-Nearest Neighbors, Matrix Factorization, Deep Learning (NCF)",
        },
        {
            "title": "Customer Churn Prediction",
            "description": (
                "Predict whether a customer is likely to stop shopping from "
                "the platform, enabling proactive retention strategies."
            ),
            "ml_type": "Supervised – Binary Classification",
            "input": [
                "Days since last purchase",
                "Average order value",
                "Number of orders in last 6 months",
                "Customer complaint count",
                "Discount / coupon usage frequency",
            ],
            "output": "Churn Status  →  'Likely to Churn' / 'Loyal Customer'  (1 / 0)",
            "algorithm": "Logistic Regression, Random Forest, XGBoost",
        },
        {
            "title": "Demand Forecasting",
            "description": (
                "Forecast the future demand for products to optimize inventory "
                "management and reduce overstock or stockouts."
            ),
            "ml_type": "Supervised – Time Series Regression",
            "input": [
                "Historical sales data (daily / weekly)",
                "Seasonal indicators (holiday, festival flags)",
                "Product category and price",
                "Marketing spend / promotional events",
                "Economic indicators (inflation rate)",
            ],
            "output": "Predicted Sales Quantity  →  Numeric forecast for next N days/weeks",
            "algorithm": "ARIMA, LSTM, Prophet, XGBoost",
        },
        {
            "title": "Sentiment Analysis on Product Reviews",
            "description": (
                "Analyze customer reviews to determine whether the sentiment "
                "is positive, negative, or neutral, helping sellers improve."
            ),
            "ml_type": "Supervised – NLP Text Classification",
            "input": [
                "Review text (raw customer review)",
                "Star rating given (1–5)",
                "Product category",
                "Review length (word count)",
                "Verified purchase flag (Yes / No)",
            ],
            "output": "Sentiment Label  →  'Positive' / 'Negative' / 'Neutral'  + Confidence Score",
            "algorithm": "Naïve Bayes, LSTM, BERT, Transformer Models",
        },
        {
            "title": "Fraud Detection in Online Transactions",
            "description": (
                "Detect fraudulent transactions in real-time to protect both "
                "the platform and customers from financial losses."
            ),
            "ml_type": "Supervised – Binary Classification (Imbalanced)",
            "input": [
                "Transaction amount (₹)",
                "Time of transaction",
                "User's device and IP address info",
                "Shipping address vs billing address match",
                "Transaction frequency in last 1 hour",
            ],
            "output": "Fraud Flag  →  'Fraudulent' / 'Legitimate'  (1 / 0)  + Risk Score (0–1)",
            "algorithm": "Isolation Forest, Random Forest, Neural Network, SMOTE + XGBoost",
        },
    ],
}


# ──────────────────────────────────────────────
#  Display Functions
# ──────────────────────────────────────────────

def print_separator(char="═", length=70):
    """Print a decorative separator line."""
    print(char * length)


def print_header():
    """Print the program header."""
    print_separator()
    print("   🤖  ML IDEA GENERATOR  🤖")
    print("   Suggesting ML Problems for College, Healthcare & Shopping")
    print_separator()
    print()


def display_idea(idea, number):
    """Display a single ML idea with full details."""
    print(f"  {'─' * 60}")
    print(f"  💡 Idea {number}: {idea['title']}")
    print(f"  {'─' * 60}")
    print(f"  📝 Description : {idea['description']}")
    print(f"  🔬 ML Type     : {idea['ml_type']}")
    print(f"  ⚙️  Algorithm   : {idea['algorithm']}")
    print()

    # Input details
    print("  📥 INPUT Features:")
    for i, inp in enumerate(idea["input"], 1):
        print(f"      {i}. {inp}")
    print()

    # Output details
    print(f"  📤 OUTPUT:")
    print(f"      → {idea['output']}")
    print()


def display_domain(domain_name, ideas):
    """Display all ideas for a given domain."""
    print()
    print_separator("─")
    emoji_map = {"College": "🎓", "Healthcare": "🏥", "Shopping": "🛒"}
    emoji = emoji_map.get(domain_name, "📌")
    print(f"  {emoji}  DOMAIN: {domain_name.upper()}")
    print_separator("─")

    for idx, idea in enumerate(ideas, 1):
        display_idea(idea, idx)


def display_all_ideas():
    """Display all ML ideas across all domains."""
    for domain_name, ideas in ml_ideas.items():
        display_domain(domain_name, ideas)

    print_separator()
    print(f"  ✅ Total ML Ideas Presented: {sum(len(v) for v in ml_ideas.values())}")
    print_separator()


def display_random_idea():
    """Pick and display one random ML idea from any domain."""
    domain = random.choice(list(ml_ideas.keys()))
    idea = random.choice(ml_ideas[domain])
    emoji_map = {"College": "🎓", "Healthcare": "🏥", "Shopping": "🛒"}
    print(f"\n  🎲 Random Pick from {emoji_map.get(domain, '')} {domain}:\n")
    display_idea(idea, 1)


def display_summary_table():
    """Display a compact summary table of all ideas."""
    print("\n" + "=" * 90)
    print(f"  {'DOMAIN':<14} {'#':<4} {'ML PROBLEM':<40} {'ML TYPE'}")
    print("=" * 90)
    for domain, ideas in ml_ideas.items():
        for i, idea in enumerate(ideas, 1):
            print(f"  {domain:<14} {i:<4} {idea['title']:<40} {idea['ml_type']}")
        print("-" * 90)
    print(f"\n  Total Ideas: {sum(len(v) for v in ml_ideas.values())}\n")


# ──────────────────────────────────────────────
#  Interactive Menu
# ──────────────────────────────────────────────

def interactive_menu():
    """Run the interactive ML Idea Generator menu."""
    print_header()

    while True:
        print("\n  ┌──────────────────────────────────┐")
        print("  │        MENU OPTIONS               │")
        print("  ├──────────────────────────────────┤")
        print("  │  1. View ALL ML Ideas             │")
        print("  │  2. View College Ideas     🎓     │")
        print("  │  3. View Healthcare Ideas  🏥     │")
        print("  │  4. View Shopping Ideas    🛒     │")
        print("  │  5. Get a Random Idea      🎲     │")
        print("  │  6. Summary Table          📊     │")
        print("  │  7. Exit                   🚪     │")
        print("  └──────────────────────────────────┘")

        choice = input("\n  Enter your choice (1-7): ").strip()

        if choice == "1":
            display_all_ideas()
        elif choice == "2":
            display_domain("College", ml_ideas["College"])
        elif choice == "3":
            display_domain("Healthcare", ml_ideas["Healthcare"])
        elif choice == "4":
            display_domain("Shopping", ml_ideas["Shopping"])
        elif choice == "5":
            display_random_idea()
        elif choice == "6":
            display_summary_table()
        elif choice == "7":
            print("\n  👋 Thank you for using ML Idea Generator! Happy Learning!\n")
            print_separator()
            break
        else:
            print("  ⚠️  Invalid choice! Please enter a number between 1 and 7.")


# ──────────────────────────────────────────────
#  Main Execution
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # Display all ideas by default (for assignment submission)
    print_header()
    display_all_ideas()

    # Also show the summary table
    display_summary_table()

    # Uncomment the line below to run the interactive menu instead:
    # interactive_menu()
