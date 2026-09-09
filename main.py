import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Ensure repository root is in Python path for clean imports
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.phishguard.predictor import analyze_url

app = FastAPI(
    title="PhishGuard AI API",
    description="Cybersecurity API for real-time AI-powered phishing detection.",
    version="1.0.0"
)

# Enable CORS for Chrome Extension & Frontend dashboard clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLAnalysisRequest(BaseModel):
    url: str
    enable_whois: bool = False

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "PhishGuard AI Backend",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze (POST)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze")
@app.post("/analyze")  # Legacy endpoint alias
def analyze_url_endpoint(payload: URLAnalysisRequest):
    if not payload.url or not payload.url.strip():
        raise HTTPException(status_code=400, detail="URL string cannot be empty.")
    
    try:
        result = analyze_url(payload.url, enable_whois=payload.enable_whois)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis engine error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting PhishGuard AI Server on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
