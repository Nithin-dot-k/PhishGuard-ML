import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib # New tool to save the model

# 1. Load data
df = pd.read_csv('phishing_data.csv')
X = df.drop('target', axis=1) 
y = df['target']

# 2. Split and Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 3. Save the model to a file
joblib.dump(model, 'phishing_model.pkl')
print("💾 Model saved as 'phishing_model.pkl'")