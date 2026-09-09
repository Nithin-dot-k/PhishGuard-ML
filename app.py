import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Ensure repository root is in Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.phishguard.predictor import analyze_url

# Page configuration
st.set_page_config(
    page_title="PhishGuard AI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Header
st.title("🛡️ PhishGuard AI Detector")
st.write("Real-time AI & Heuristic Phishing Detection System")

url_input = st.text_input("Enter website URL to analyze:", placeholder="https://example.com")

if st.button("Analyze URL", type="primary"):
    if url_input:
        with st.spinner("Analyzing URL structure and risk factors..."):
            try:
                res = analyze_url(url_input, enable_whois=False)
                risk_score = res['risk_score']
                verdict = res['verdict']
                threat_factors = res['threat_factors']
                
                st.divider()
                st.subheader("Analysis Summary")
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    st.metric("Final Risk Score", f"{risk_score}%")
                
                with col2:
                    if risk_score >= 70:
                        st.error(f"🚨 {verdict}")
                    elif risk_score >= 40:
                        st.warning(f"⚠️ {verdict}")
                    else:
                        st.success(f"✅ {verdict}")
                        
                with col3:
                    st.write("**Threat Confidence Meter**")
                    st.progress(risk_score / 100.0)
                
                st.write("### 🔍 Threat Factors & Key Signals")
                if threat_factors:
                    for factor in threat_factors:
                        st.write(f"🚩 **Flag:** {factor}")
                else:
                    st.write("🟢 No critical threat flags detected.")
                
                if res['is_whitelisted']:
                    st.info("ℹ️ Domain is verified on the trusted domain whitelist.")
                elif res['is_brand_spoof']:
                    st.warning("⚠️ Brand impersonation detected on unverified domain.")
                    
                with st.expander("View Feature Matrix"):
                    df_feats = pd.DataFrame([res['features']])
                    st.dataframe(df_feats)
                    
            except Exception as e:
                st.error(f"Analysis Error: {str(e)}")
    else:
        st.info("Please enter a URL above.")

st.markdown("---")
st.caption("Built with FastAPI, Scikit-Learn & Streamlit | PhishGuard AI Project")