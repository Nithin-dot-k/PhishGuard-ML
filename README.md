# 🛡️ PhishGuard AI: Real-Time Phishing Detection

An Intelligent Machine Learning-based URL scanner that detects phishing attempts using behavioral and structural analysis.

## 🚀 Features

- **Machine Learning Engine:** Powered by a Random Forest Classifier.
- **Real-Time Feature Extraction:** Automatically analyzes URL length, HTTPS status, and symbol presence.
- **Cyber Intelligence:** Integrates WHOIS lookups to determine domain age (a key indicator of phishing).
- **Modern Web UI:** Built with Streamlit for a seamless user experience.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **ML Library:** Scikit-Learn
- **Web Framework:** Streamlit
- **Data Handling:** Pandas, Joblib
- **Network Tools:** python-whois, tldextract

## 📊 How it Works

The model is trained on a "Hardened Dataset" containing both legitimate and malicious URLs. It evaluates 5 key features:

1. URL Length
2. Presence of '@' symbols
3. HTTPS Protocol status
4. Subdomain/Dot count
5. **Domain Age (Days since registration)**

## 🚦 Usage

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

---

_Developed as a Portfolio Project by Nithin (2026)_
