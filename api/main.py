import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to sys.path for Vercel serverless context
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.phishguard.predictor import analyze_url

app = FastAPI(
    title="PhishGuard Serverless API",
    description="Vercel serverless endpoint for PhishGuard AI"
)

# Enable CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "PhishGuard Vercel API is running"}

@app.post("/api/main/analyze")
@app.post("/api/analyze")
async def analyze(request: URLRequest):
    try:
        # Vercel serverless operates without WHOIS to ensure fast execution (<500ms)
        result = analyze_url(request.url, enable_whois=False)
        return result
    except Exception as e:
        return {
            "url": request.url,
            "risk_score": -1,
            "error": str(e)
        }