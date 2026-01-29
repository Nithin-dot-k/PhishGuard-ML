# 🛡️ PhishGuard: AI-Powered Phishing Detection System

PhishGuard is a high-performance cybersecurity tool that combines **Machine Learning** with **Heuristic Analysis** to detect phishing websites in real-time. It consists of a FastAPI backend running a Random Forest model and a Chrome Extension for a seamless user experience.

## 🚀 Key Features

- **AI-Driven Analysis:** Uses a Random Forest Classifier to evaluate URL structure and domain age.
- **Hybrid Detection:** Employs a Heuristic Layer (Brand Boosting) to catch spoofing attempts on brands like Amazon and PayPal.
- **Whitelist Layer:** Zero-latency trust for verified domains (Google, GitHub, etc.).
- **Real-time Protection:** Chrome Extension interface provides instant risk scores while browsing.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI/ML:** Scikit-learn, Pandas, Joblib
- **Frontend:** JavaScript (Chrome Extension API), HTML5, CSS3
- **Data:** TLDextract, Python-Whois

## 📐 Architecture

1. **User** visits a website.
2. **Chrome Extension** captures the URL and sends it to the **FastAPI Server**.
3. **Server** checks the **Whitelist**.
4. If not whitelisted, the **AI Model** predicts risk based on 5 features (Length, Dots, HTTPS, etc.).
5. **Heuristic Engine** checks for brand impersonation and adjusts the score dynamically.
6. **Risk Score** is returned and displayed in a color-coded UI.

## 🔧 Installation & Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone [https://github.com/your-username/PhishGuard.git](https://github.com/your-username/PhishGuard.git)
cd PhishGuard

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the AI Engine
python main.py
```
