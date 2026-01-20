import streamlit as st
import joblib
import pandas as pd
import tldextract
import whois
from datetime import datetime

# 1. Load the trained brain
# Make sure phishing_model.pkl is in the same folder!
model = joblib.load('phishing_model.pkl')

# 2. Page Configuration
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️")

st.title("🛡️ PhishGuard: AI Phishing Detector")
st.write("This tool uses Machine Learning to analyze URLs for phishing threats.")

# 3. Domain Age Function (with the Timezone Fix)
def get_domain_age_in_days(url):
    try:
        ext = tldextract.extract(url)
        domain_name = f"{ext.domain}.{ext.suffix}"
        w = whois.whois(domain_name)
        
        res = w.creation_date
        if isinstance(res, list):
            creation_date = res[0]
        else:
            creation_date = res
            
        if creation_date:
            # The Timezone Fix: Make the date naive
            if hasattr(creation_date, 'tzinfo') and creation_date.tzinfo is not None:
                creation_date = creation_date.replace(tzinfo=None)
            
            age_days = (datetime.now() - creation_date).days
            return age_days
        return 0
    except:
        return 0

# 4. User Input
url_input = st.text_input("Paste a URL to analyze:", "https://")

if st.button("Analyze URL"):
    with st.spinner('🔍 Analyzing domain registry and URL patterns...'):
        # Feature Extraction
        length = len(url_input)
        at_symbol = 1 if '@' in url_input else 0
        https = 1 if url_input.startswith('https') else 0
        dots = url_input.count('.')
        age = get_domain_age_in_days(url_input)
        
        # Prepare data for model
        features = [length, at_symbol, https, dots, age]
        cols = ['url_length', 'has_at_symbol', 'has_https', 'no_of_dots', 'domain_age_days']
        df_input = pd.DataFrame([features], columns=cols)
        
        # Prediction
        prediction = model.predict(df_input)
        
        st.divider()
        
        # Display Result
        if prediction[0] == 1:
            st.error(f"🚨 ALERT: This URL is likely PHISHING!")
            st.warning(f"Reasoning: Domain age is {age} days and URL patterns are suspicious.")
        else:
            st.success(f"✅ SAFE: This URL appears to be legitimate.")
            st.info(f"Domain age: {age} days ({round(age/365, 1)} years)")

        # Show the "Clues" to the user
        st.write("### Technical Clues Extracted:")
        st.dataframe(df_input)

st.markdown("---")
st.caption("Built by Nithin | PhishGuard ML Project 2026")