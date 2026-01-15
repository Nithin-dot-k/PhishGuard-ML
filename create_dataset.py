import pandas as pd

# Expanded dataset with "Edge Cases"
# 1 = Phishing, 0 = Legitimate
data = {
    'url_length': [15, 80, 22, 110, 18, 95, 25, 120, 60, 55, 12, 115, 70, 20, 150, 45],
    'has_at_symbol': [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1],
    'has_https': [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    'no_of_dots': [1, 5, 1, 4, 2, 6, 1, 5, 2, 3, 1, 6, 2, 1, 8, 2],
    'target': [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1] 
}

df = pd.DataFrame(data)
df.to_csv('phishing_data.csv', index=False)

print("✅ Hardened dataset 'phishing_data.csv' created with 16 examples!")