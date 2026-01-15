import pandas as pd
import os

file_path = 'phishing_data.csv'

if os.path.exists(file_path):
    # Load the local file
    data = pd.read_csv(file_path)
    print("📂 Local Dataset Loaded Successfully!")
    
    print("\n--- Dataset Preview ---")
    print(data.head())
    
    print("\n--- Class Distribution ---")
    # 0 = Safe, 1 = Phishing
    print(data['target'].value_counts())
else:
    print("❌ Error: 'phishing_data.csv' not found. Run create_dataset.py first!")