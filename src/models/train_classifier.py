import os
import sys
import subprocess
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ----------------------------
# Set tracking URI via env var
# MUST be before mlflow is used
# ----------------------------
os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///mlflow.db"

# ----------------------------
# Create required folders
# ----------------------------
os.makedirs("src/models", exist_ok=True)

# ----------------------------
# MLflow setup
# ----------------------------
mlflow.set_experiment("Finance_Transaction_Classifier")

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("data/training/transactions.csv")

X = df["description"]
y = df["category"]

# ----------------------------
# Train-test split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ----------------------------
# Start MLflow run
# ----------------------------
with mlflow.start_run():

    # Model pipeline
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    # Train model
    model.fit(X_train, y_train)

    # Predict
    preds = model.predict(X_test)

    # Evaluate
    accuracy = accuracy_score(y_test, preds)
    print(f"Accuracy: {accuracy:.4f}")

    # ----------------------------
    # Log to MLflow
    # ----------------------------
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("max_iter", 1000)
    mlflow.log_param("test_size", 0.2)
    mlflow.sklearn.log_model(model, "classifier")

    # ----------------------------
    # Save locally
    # ----------------------------
    joblib.dump(model, "src/models/category_model.pkl")

    # Print run id
    run_id = mlflow.active_run().info.run_id
    print("MLflow Run ID:", run_id)

print("Training completed successfully 🚀")

# ----------------------------
# Launch MLflow UI
# Uses same Python interpreter (fixes version mismatch error)
# ----------------------------
if not os.getenv("CI"):
    print("Starting MLflow UI → open http://127.0.0.1:5000 in your browser")
    subprocess.Popen([
        sys.executable, "-m", "mlflow", "ui",
        "--backend-store-uri", "sqlite:///mlflow.db",
        "--port", "5000"
    ])