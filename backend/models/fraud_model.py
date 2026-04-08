import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_PATH = "data/processed/fraud_isolation_forest.joblib"


def train_isolation_forest(train_csv: str, contamination: float = 0.01):
    df = pd.read_csv(train_csv)
    # Expect data to include a 'Class' column (0 normal, 1 fraud) - drop label for unsupervised training
    X = df.drop(columns=[col for col in df.columns if col == "Class"], errors="ignore")
    model = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    return joblib.load(MODEL_PATH)


def predict(model, X):
    # IsolationForest.predict returns 1 for normal, -1 for anomaly
    preds = model.predict(X)
    scores = model.decision_function(X)
    return preds, scores
