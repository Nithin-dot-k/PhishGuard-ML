import os
from pathlib import Path
import joblib
import pandas as pd
from .feature_extractor import extract_features_df, FEATURE_COLUMNS
from .heuristic_engine import apply_heuristics

# Define candidate model paths in order of preference
ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATHS = [
    ROOT_DIR / "models" / "phishing_model.pkl",
    ROOT_DIR / "api" / "phishing_model.pkl",
    ROOT_DIR / "phishing_model.pkl",
]

_model_cache = None

def get_model_path() -> Path:
    """Finds the first existing model artifact path."""
    for path in MODEL_PATHS:
        if path.exists():
            return path
    # Default to models directory path if none exist yet
    return MODEL_PATHS[0]

def load_phishing_model():
    """Loads and caches the Scikit-Learn trained RandomForestClassifier."""
    global _model_cache
    if _model_cache is not None:
        return _model_cache
    
    path = get_model_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Phishing model file not found at '{path}'. Please run 'python models/train_model.py' first."
        )
    
    _model_cache = joblib.load(path)
    return _model_cache

def analyze_url(url: str, enable_whois: bool = False) -> dict:
    """
    Full inference pipeline for a URL:
    1. Extracts feature vector.
    2. Runs model inference to get base probability score.
    3. Applies whitelist and brand spoofing heuristics.
    4. Formats clean response schema.
    """
    model = load_phishing_model()
    
    # Extract features
    df_features = extract_features_df(url, enable_whois=enable_whois)
    
    # Predict probability of phishing (class 1)
    probabilities = model.predict_proba(df_features)[0]
    base_score = int(round(probabilities[1] * 100))
    
    # Apply Heuristics
    heuristic_res = apply_heuristics(url, base_score)
    
    # Extract threat factors for UI visibility
    row = df_features.iloc[0]
    threat_factors = []
    if row['has_https'] == 0:
        threat_factors.append("No HTTPS Encryption")
    if row['has_at_symbol'] == 1:
        threat_factors.append("Contains '@' Symbol")
    if row['has_ip'] == 1:
        threat_factors.append("Raw IP Address Host")
    if row['no_of_dots'] > 3:
        threat_factors.append(f"High Dot Count ({row['no_of_dots']})")
    if row['hyphen_count'] > 2:
        threat_factors.append(f"Multiple Hyphens ({row['hyphen_count']})")
    if heuristic_res['is_brand_spoof']:
        threat_factors.append("Brand Keywords on Untrusted Domain")
        
    return {
        "url": url,
        "risk_score": heuristic_res['risk_score'],
        "base_score": base_score,
        "verdict": heuristic_res['verdict'],
        "is_whitelisted": heuristic_res['is_whitelisted'],
        "is_brand_spoof": heuristic_res['is_brand_spoof'],
        "threat_factors": threat_factors,
        "features": row.to_dict()
    }
