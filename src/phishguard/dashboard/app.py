import pandas as pd
import streamlit as st

from phishguard.predictor import analyze_url


st.set_page_config(
    page_title="PhishGuard AI Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ PhishGuard AI Detector")
st.write("Real-time AI & Heuristic Phishing Detection System")

url_input = st.text_input("Enter website URL to analyze:", placeholder="https://example.com")

if st.button("Analyze URL", type="primary"):
    if url_input:
        with st.spinner("Analyzing URL structure and risk factors..."):
            try:
                result = analyze_url(url_input, enable_whois=False)
                risk_score = result["risk_score"]

                st.divider()
                st.subheader("Analysis Summary")
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    st.metric("Final Risk Score", f"{risk_score}%")
                with col2:
                    if risk_score >= 70:
                        st.error(f"🚨 {result['verdict']}")
                    elif risk_score >= 40:
                        st.warning(f"⚠️ {result['verdict']}")
                    else:
                        st.success(f"✅ {result['verdict']}")
                with col3:
                    st.write("**Threat Confidence Meter**")
                    st.progress(risk_score / 100.0)

                st.write("### 🔍 Threat Factors & Key Signals")
                if result["threat_factors"]:
                    for factor in result["threat_factors"]:
                        st.write(f"🚩 **Flag:** {factor}")
                else:
                    st.write("🟢 No critical threat flags detected.")

                if result["is_whitelisted"]:
                    st.info("ℹ️ Domain is verified on the trusted domain whitelist.")
                elif result["is_brand_spoof"]:
                    st.warning("⚠️ Brand impersonation detected on unverified domain.")

                with st.expander("View Feature Matrix"):
                    st.dataframe(pd.DataFrame([result["features"]]))
            except Exception as exc:
                st.error(f"Analysis Error: {exc}")
    else:
        st.info("Please enter a URL above.")

st.markdown("---")
st.caption("Built with FastAPI, Scikit-Learn & Streamlit | PhishGuard AI Project")
