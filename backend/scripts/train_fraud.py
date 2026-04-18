import pandas as pd
import joblib
import os
from backend.models.fraud_model import FraudModel

def train():
    data_path = r"C:\Users\vadde\Desktop\bank\bank_support_ai11\data\kaggle\b"
    
    if not os.path.exists(data_path):
        print("❌ Dataset missing.")
        return

    print("📖 Loading data...")
    df = pd.read_csv(data_path)
    model = FraudModel()
    
    # Use standard features for Isolation Forest
    features = [f'V{i}' for i in range(1, 29)] + ['Amount']
    
    print("⚙️ Training Fraud Model...")
    model.train(df[features])
    
    os.makedirs("data/processed", exist_ok=True)
    model.save("data/processed/fraud_isolation_forest.joblib")
    print("✅ Model trained successfully.")

if __name__ == "__main__":
    train()