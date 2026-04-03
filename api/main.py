from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import re
import os
from urllib.parse import urlparse

app = FastAPI()

# ✅ CORS — required for Chrome extension to receive the response
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# ✅ Load model using absolute path (required for Vercel serverless)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "phishing_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

class URLRequest(BaseModel):
    url: str

# ✅ Match EXACTLY the features your model was trained on
def extract_features(url: str):
    parsed = urlparse(url)
    return [[
        len(url),                                              # url_length
        url.count('.'),                                        # dot_count
        1 if parsed.scheme == 'https' else 0,                 # has_https
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,  # has_ip
        url.count('-'),                                        # hyphen_count
    ]]

@app.get("/")
def root():
    return {"status": "PhishGuard API is running", "model_loaded": model_loaded}

@app.post("/api/main/analyze")
async def analyze(request: URLRequest):
    if not model_loaded:
        return {
            "url": request.url,
            "risk_score": -1,
            "error": f"Model failed to load: {model_error}"
        }
    try:
        features = extract_features(request.url)
        probability = model.predict_proba(features)[0][1]
        risk_score = round(probability * 100)

        return {
            "url": request.url,
            "risk_score": risk_score   # ✅ exact key your popup.js reads
        }
    except Exception as e:
        return {
            "url": request.url,
            "risk_score": -1,
            "error": str(e)
        }