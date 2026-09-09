import sys
import shutil
from pathlib import Path

# Add repository root to sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

DATA_PATH = BASE_DIR / "data" / "raw" / "phishing_data.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "phishing_model.pkl"
VERCEL_MODEL_PATH = BASE_DIR / "api" / "phishing_model.pkl"

def train():
    # Generate dataset if not present
    if not DATA_PATH.exists():
        print("Data file not found. Generating dataset first...")
        from data.create_dataset import create_dataset
        create_dataset()

    df = pd.read_csv(DATA_PATH)
    X = df.drop('target', axis=1)
    y = df['target']

    print(f"[INFO] Training RandomForestClassifier on features: {X.columns.tolist()}")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save to models directory
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[SUCCESS] Model saved to '{MODEL_PATH}'")

    # Sync to Vercel API directory
    VERCEL_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(MODEL_PATH, VERCEL_MODEL_PATH)
    print(f"[SUCCESS] Model copied to Vercel API directory at '{VERCEL_MODEL_PATH}'")

if __name__ == "__main__":
    train()
