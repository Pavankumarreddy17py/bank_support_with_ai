"""Simple script to train a fraud IsolationForest model.
Usage:
    python backend/scripts/train_fraud.py data/kaggle/creditcard.csv
"""
import sys
from backend.models.fraud_model import train_isolation_forest


def main():
    if len(sys.argv) < 2:
        print("Usage: python train_fraud.py <path-to-csv>")
        return
    csv = sys.argv[1]
    model = train_isolation_forest(csv)
    print("Trained model and saved to data/processed/")

if __name__ == "__main__":
    main()
