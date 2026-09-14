import shutil
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "raw" / "phishing_data.csv"
MODEL_PATH = ROOT_DIR / "models" / "phishing_model.pkl"
DEPLOYMENT_MODEL_PATH = ROOT_DIR / "api" / "phishing_model.pkl"


def train() -> None:
    if not DATA_PATH.exists():
        from create_dataset import create_dataset

        create_dataset()

    data = pd.read_csv(DATA_PATH)
    features = data.drop("target", axis=1)
    target = data["target"]

    print(f"[INFO] Training on features: {features.columns.tolist()}")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, target)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    shutil.copy2(MODEL_PATH, DEPLOYMENT_MODEL_PATH)
    print(f"[SUCCESS] Model saved to '{MODEL_PATH}'")
    print(f"[SUCCESS] Deployment copy saved to '{DEPLOYMENT_MODEL_PATH}'")


if __name__ == "__main__":
    train()
