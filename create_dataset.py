import pandas as pd

# Hardened dataset with 5 features + 1 target
data = {
    'url_length': [15, 80, 22, 110, 18, 95, 25, 120, 60, 55, 12, 115, 70, 20, 150, 45],
    'has_at_symbol': [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1],
    'has_https': [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    'no_of_dots': [1, 5, 1, 4, 2, 6, 1, 5, 2, 3, 1, 6, 2, 1, 8, 2],
    'domain_age_days': [5000, 5, 4000, 10, 3500, 2, 6000, 1, 15, 20, 4500, 5, 3000, 5000, 1, 12],
    'target': [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1] 
}

df = pd.DataFrame(data)
df.to_csv('phishing_data.csv', index=False)
print("✅ CSV UPDATED! Now has 5 features.")