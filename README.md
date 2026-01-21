# 🛡️ PhishGuard AI: Threat Analysis Dashboard

PhishGuard is an Intelligent Machine Learning-based URL scanner that detects phishing attempts using behavioral, structural, and heuristic analysis.

## 🚀 Key Features

- **Explainable AI (XAI) Dashboard**: Instead of a simple "Yes/No," the app provides a **Risk Percentage** and explains the specific threat factors (e.g., "New Domain," "No HTTPS").
- **Machine Learning Engine**: Powered by a **Random Forest Classifier** trained on URL structural patterns.
- **Heuristic Brand Detection**: Specifically identifies "Social Engineering" attempts by scanning for brand keywords (Paypal, Bank, etc.) in suspicious domains.
- **Cyber Intelligence Integration**: Real-time **WHOIS lookups** fetch domain seniority with timezone-naive normalization for accurate risk weighting.
- **Interactive UI**: Built with Streamlit, featuring a dynamic **Risk Gauge** for immediate visual alerts.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **ML Library**: Scikit-Learn (Random Forest)
- **Web Framework**: Streamlit
- **Network Tools**: `python-whois`, `tldextract`
- **Data Handling**: Pandas, Joblib

## 📊 How It Works

1. **Feature Extraction**: The app extracts 5 key features from the URL (Length, Dots, Symbols, HTTPS, and Domain Age).
2. **Probability Scoring**: The Random Forest model calculates a confidence score based on trained patterns.
3. **Risk Boosting**: A heuristic layer checks for brand spoofing and boosts the risk score if sensitive keywords are detected.
4. **Visual Verdict**: The user receives a color-coded assessment (Low/Medium/High Risk).

## 🚦 Usage

1. **Clone the repo**
2. **Install dependencies**:  
   `pip install -r requirements.txt`
3. **Run the app**:  
   `streamlit run app.py`
