import joblib
import pandas as pd

# 1. Load the saved brain
model = joblib.load('phishing_model.pkl')

print("🛡️ PhishGuard Scanner Active")

# 2. Get input from the user (The Detective)
print("\nEnter the URL features to scan:")
length = int(input("URL Length (e.g., 20 or 100): "))
at_symbol = int(input("Has '@' symbol? (1 for Yes, 0 for No): "))
https = int(input("Has HTTPS? (1 for Yes, 0 for No): "))
dots = int(input("Number of dots in URL: "))

# 3. Format the input for the model
user_input = pd.DataFrame([[length, at_symbol, https, dots]], 
                          columns=['url_length', 'has_at_symbol', 'has_https', 'no_of_dots'])

# 4. Make a prediction
prediction = model.predict(user_input)

if prediction[0] == 1:
    print("\n🚨 WARNING: This looks like a PHISHING URL!")
else:
    print("\n✅ SAFE: This URL looks legitimate.")