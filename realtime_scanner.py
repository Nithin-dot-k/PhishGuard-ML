import joblib
import pandas as pd
import tldextract

# 1. Load the saved brain
model = joblib.load('phishing_model.pkl')

def extract_features(url):
    """Turns a raw URL string into numbers the model understands"""
    # Feature 1: URL Length
    length = len(url)
    
    # Feature 2: Has '@' symbol
    at_symbol = 1 if '@' in url else 0
    
    # Feature 3: Has HTTPS
    # Most phishing sites in our tiny dataset used 'http' (0)
    https = 1 if url.startswith('https') else 0
    
    # Feature 4: Number of dots
    dots = url.count('.')
    
    return [length, at_symbol, https, dots]

print("🚀 Real-Time PhishGuard Scanner")
print("-------------------------------")

# 2. Get a REAL URL from the user
user_url = input("Paste a URL to scan (e.g., https://google.com): ")

# 3. Extract the features automatically
features = extract_features(user_url)

# 4. Convert to DataFrame for the model
# Use the EXACT same column names as our training data
feature_names = ['url_length', 'has_at_symbol', 'has_https', 'no_of_dots']
data_for_model = pd.DataFrame([features], columns=feature_names)

# 5. Predict
prediction = model.predict(data_for_model)

print(f"\nAnalysis for: {user_url}")
print(f"Extracted Features: {features}")

if prediction[0] == 1:
    print("🚨 RESULT: This URL is highly suspicious (PHISHING)!")
else:
    print("✅ RESULT: This URL appears to be SAFE.")