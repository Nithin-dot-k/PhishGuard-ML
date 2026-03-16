from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import tldextract
import whois
from datetime import datetime
import uvicorn

app = FastAPI()

# Fix CORS errors so the Browser Extension can talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. LOAD AI MODEL ---
print("🚀 Loading AI Model...")
try:
    model = joblib.load('phishing_model.pkl')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ ERROR loading model: {e}")

# --- 2. CONFIGURATION ---
SUSPICIOUS_KEYWORDS = ['paypal', 'login', 'verify', 'bank', 'secure', 'update', 'account', 'signin', 'amazon', 'netflix', 'microsoft', 'google']
WHITELIST = ['google.com', 'github.com', 'microsoft.com', 'stackoverflow.com', 'gemini.google.com', 'openai.com', 'amazon.com', 'paypal.com']

class UrlRequest(BaseModel):
    url: str

def get_age(url):
    """Safely calculate domain age in days."""
    try:
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"
        w = whois.whois(domain)
        date = w.creation_date
        
        if isinstance(date, list): 
            date = date[0]
        if date is None:
            return 0
            
        if hasattr(date, 'tzinfo') and date.tzinfo is not None: 
            date = date.replace(tzinfo=None)
        
        age = (datetime.now() - date).days
        return max(age, 0) 
    except Exception:
        return 0

@app.get("/")
def home():
    return {"message": "PhishGuard Server is Running!"}

@app.post("/analyze")
async def analyze_url(request: UrlRequest):
    url = request.url.lower()
    print(f"\n🔍 Analyzing: {url}")
    
    # --- 3. WHITELIST CHECK ---
    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"
    if domain in WHITELIST:
        print(f"✅ Whitelisted domain: {domain}")
        return {
            "url": url,
            "risk_score": 0,
            "is_brand_spoof": False,
            "age_days": 9999
        }

    # --- 4. FEATURE EXTRACTION ---
    age = get_age(url)
    has_brand_keyword = 1 if any(word in url for word in SUSPICIOUS_KEYWORDS) else 0
    
    features = [
        len(url),
        1 if '@' in url else 0,
        1 if url.startswith('https') else 0,
        url.count('.'),
        age
    ]
    
    # --- 5. AI PREDICTION ---
    df_input = pd.DataFrame([features], columns=['url_length', 'has_at_symbol', 'has_https', 'no_of_dots', 'domain_age_days'])
    probabilities = model.predict_proba(df_input)[0]
    
    # Probability of being phishing (class 1)
    risk_score = int(probabilities[1] * 100)
    print(f"📊 AI Base Score: {risk_score}%")

    # --- 6. DYNAMIC BRAND BOOST ---
    # Instead of a flat +40, we use a multiplier for a more realistic range
    if has_brand_keyword:
        # Increase the risk by 50% of its current value
        risk_score = int(risk_score * 1.5)
        
        # Ensure that if it has a brand keyword but isn't whitelisted, 
        # it hits at least a "Medium-High" risk floor
        if risk_score < 60:
            risk_score = 65
        
        print(f"🚩 Brand Keyword Detected. Dynamic Score: {min(risk_score, 100)}%")
    
    final_score = min(risk_score, 100)
    print(f"🎯 Final Verdict: {final_score}% Risk")
    
    return {
        "url": url,
        "risk_score": final_score,
        "age_days": age,
        "is_brand_spoof": bool(has_brand_keyword)
    }

# if __name__ == "__main__":
#     print("📡 PhishGuard Engine starting on http://127.0.0.1:8000")
#     uvicorn.run(app, host="127.0.0.1", port=8000)


