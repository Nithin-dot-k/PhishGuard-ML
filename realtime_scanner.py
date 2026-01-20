import joblib
import pandas as pd
import tldextract
import whois
from datetime import datetime
import time

# 1. Load the saved brain
model = joblib.load('phishing_model.pkl')

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
            # FIX: If the date has timezone info (aware), strip it (make it naive)
            if creation_date.tzinfo is not None:
                creation_date = creation_date.replace(tzinfo=None)
            
            age_days = (datetime.now() - creation_date).days
            return age_days
        return 0
    except Exception as e:
        # This will now tell us if it's a real error or just a missing date
        print(f"🔍 Info: Could not calculate age for {domain_name}. Defaulting to 0.")
        return 0

def extract_features(url):
    """Now extracting 5 features instead of 4!"""
    length = len(url)
    at_symbol = 1 if '@' in url else 0
    https = 1 if url.startswith('https') else 0
    dots = url.count('.')
    
    # NEW FEATURE: Domain Age
    age = get_domain_age_in_days(url)
    
    return [length, at_symbol, https, dots, age]

# --- Scanner UI ---
print("🚀 Real-Time PhishGuard (Advanced Edition)")
print("-----------------------------------------")

user_url = input("Paste a URL to scan: ")
features = extract_features(user_url)

# Note: We must update the feature names to match the 5 features now!
feature_names = ['url_length', 'has_at_symbol', 'has_https', 'no_of_dots', 'domain_age_days']
data_for_model = pd.DataFrame([features], columns=feature_names)

prediction = model.predict(data_for_model)

print(f"\n[REPORT]")
print(f"Domain Age: {features[4]} days")
print(f"Verdict: {'🚨 PHISHING' if prediction[0] == 1 else '✅ SAFE'}")