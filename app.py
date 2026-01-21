import streamlit as st
import joblib
import pandas as pd
import tldextract
import whois
from datetime import datetime

# --- 1. SETUP ---
model = joblib.load('phishing_model.pkl')
st.set_page_config(page_title="PhishGuard AI Dashboard", page_icon="🛡️", layout="wide")

def get_age(url):
    try:
        ext = tldextract.extract(url)
        w = whois.whois(f"{ext.domain}.{ext.suffix}")
        date = w.creation_date
        if isinstance(date, list): date = date[0]
        if date.tzinfo is not None: date = date.replace(tzinfo=None)
        return (datetime.now() - date).days
    except: return 0

SUSPICIOUS_KEYWORDS = ['paypal', 'login', 'verify', 'bank', 'secure', 'update', 'account', 'signin']

# --- 2. UI HEADER ---
st.title("🛡️ PhishGuard AI Detector")
st.write("Machine Learning and Heuristic Analysis Dashboard")

url_input = st.text_input("Paste a URL to analyze:", placeholder="http://example.com")

if st.button("Analyze URL"):
    if url_input:
        with st.spinner('Calculating Risk...'):
            # Data Extraction
            age = get_age(url_input)
            has_brand_keyword = 1 if any(word in url_input.lower() for word in SUSPICIOUS_KEYWORDS) else 0
            features = [len(url_input), 1 if '@' in url_input else 0, 1 if url_input.startswith('https') else 0, url_input.count('.'), age]
            
            df_input = pd.DataFrame([features], columns=['url_length', 'has_at_symbol', 'has_https', 'no_of_dots', 'domain_age_days'])
            
            # Prediction & Logic
            prob = model.predict_proba(df_input)[0][1]
            risk_score = int(prob * 100)
            if has_brand_keyword and risk_score < 85:
                risk_score += 15
                if risk_score > 100: risk_score = 100

            st.divider()

            # --- 3. THE "DASHBOARD" LAYOUT (Back to Columns!) ---
            st.subheader("Final Risk Assessment")
            col1, col2, col3 = st.columns([1, 1, 2]) # [Metric, Metric, Progress Bar]
            
            with col1:
                st.metric("Risk Score", f"{risk_score}%")
            
            with col2:
                if risk_score > 70:
                    st.error("HIGH RISK")
                elif risk_score > 30:
                    st.warning("SUSPICIOUS")
                else:
                    st.success("SAFE")

            with col3:
                st.write("**Threat Confidence Level**")
                st.progress(risk_score / 100)

            # --- 4. THREAT FACTORS (Side-by-Side) ---
            st.write("### 🔍 Threat Factors Identified")
            c1, c2 = st.columns(2)
            with c1:
                if age < 365:
                    st.write(f"🚩 **Domain Age:** New domain ({age} days).")
                else:
                    st.write(f"🟢 **Domain Age:** Established ({age} days).")
                
                if features[2] == 0:
                    st.write("🚩 **Security:** No HTTPS encryption found.")
            
            with c2:
                if has_brand_keyword:
                    st.write("🚩 **Brand Spoofing:** Suspicious keywords detected.")
                if features[3] > 3:
                    st.write(f"🚩 **Complexity:** High dot count ({features[3]}).")

            with st.expander("View Technical Feature Vector"):
                st.dataframe(df_input)

st.markdown("---")
st.caption("Built by Nithin | PhishGuard ML Project 2026")