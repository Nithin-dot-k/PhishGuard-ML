from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from phishguard.api.schemas import URLAnalysisRequest
from phishguard.predictor import analyze_url


def create_app() -> FastAPI:
    app = FastAPI(
        title="PhishGuard AI API",
        description="Cybersecurity API for real-time AI-powered phishing detection.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.get("/")
    def read_root() -> dict:
        return {
            "status": "online",
            "service": "PhishGuard AI Backend",
            "version": "1.0.0",
            "endpoints": {
                "analyze": "/api/analyze (POST)",
                "health": "/health (GET)",
            },
        }

    @app.get("/health")
    def health_check() -> dict:
        return {"status": "healthy"}

    @app.post("/api/analyze")
    @app.post("/api/main/analyze")
    @app.post("/analyze")
    def analyze_url_endpoint(payload: URLAnalysisRequest) -> dict:
        if not payload.url.strip():
            raise HTTPException(status_code=400, detail="URL string cannot be empty.")

        try:
            return analyze_url(payload.url, enable_whois=payload.enable_whois)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail="Analysis engine error.",
            ) from exc

    return app


app = create_app()
