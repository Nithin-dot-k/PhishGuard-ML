import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('phishing_data.csv')
X = df.drop('target', axis=1) # Features (now 5 of them!)
y = df['target'] # Label

print(f"🧠 Training on clues: {X.columns.tolist()}")

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, 'phishing_model.pkl')
print("✅ Model RE-TRAINED and saved!")