"""Load data/kaggle/creditcard.csv, train IsolationForest, and compute validation metrics.
Writes results to data/processed/fraud_validation.json

Usage:
    python backend/scripts/validate_fraud_on_kaggle.py
"""
import os
import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import StratifiedShuffleSplit

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'kaggle')
CSV_PATH = os.path.join(DATA_DIR, 'creditcard.csv')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, 'fraud_validation.json')

if not os.path.exists(CSV_PATH):
    raise SystemExit(f"Dataset not found at {CSV_PATH}. Run download script first.")

print('Loading dataset:', CSV_PATH)
df = pd.read_csv(CSV_PATH)
if 'Class' not in df.columns:
    raise SystemExit('Dataset missing Class label column')

# Basic checks
n_rows = len(df)
class_counts = df['Class'].value_counts().to_dict()
print('Rows:', n_rows, 'Class distribution:', class_counts)

# Prepare features and labels
X = df.drop(columns=['Class'], errors='ignore')
y = df['Class'].astype(int).values

# Stratified split so test has positives
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
train_idx, test_idx = next(sss.split(X, y))
X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

print('Train size:', len(X_train), 'Test size:', len(X_test))

# Train IsolationForest on training data (unsupervised)
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(X_train)

# Predict on test set
preds = model.predict(X_test)
y_pred = (preds == -1).astype(int)

# Compute metrics
accuracy = float(accuracy_score(y_test, y_pred))
precision = float(precision_score(y_test, y_pred, zero_division=0))
recall = float(recall_score(y_test, y_pred, zero_division=0))
f1 = float(f1_score(y_test, y_pred, zero_division=0))
cm = confusion_matrix(y_test, y_pred).tolist()

report = {
    'rows': int(n_rows),
    'class_counts': class_counts,
    'train_size': int(len(X_train)),
    'test_size': int(len(X_test)),
    'metrics': {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
    }
}

with open(OUT_PATH, 'w') as f:
    json.dump(report, f, indent=2)

print('Validation complete. Report written to', OUT_PATH)
print(json.dumps(report['metrics'], indent=2))
