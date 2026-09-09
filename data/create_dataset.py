import os
import pandas as pd
from pathlib import Path

# Target file paths
DATA_DIR = Path(__file__).resolve().parent / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = DATA_DIR / "phishing_data.csv"

# Dataset with 7 unified features + 1 target label (0 = Safe, 1 = Phishing)
data = {
    'url_length':      [15,  80, 22, 110, 18, 95, 25, 120, 60, 55, 12, 115, 70, 20, 150, 45, 30, 85, 14, 105],
    'has_at_symbol':   [ 0,   1,  0,   1,  0,  0,  0,   1,  1,  1,  0,   1,  0,  0,   1,  1,  0,  1,  0,   1],
    'has_https':       [ 1,   0,  1,   0,  1,  0,  1,   0,  0,  0,  1,   0,  1,  1,   0,  0,  1,  0,  1,   0],
    'no_of_dots':      [ 1,   5,  1,   4,  2,  6,  1,   5,  2,  3,  1,   6,  2,  1,   8,  2,  1,  4,  1,   5],
    'has_ip':          [ 0,   0,  0,   1,  0,  0,  0,   1,  0,  0,  0,   1,  0,  0,   1,  0,  0,  1,  0,   0],
    'hyphen_count':    [ 0,   3,  0,   4,  0,  2,  0,   3,  1,  2,  0,   4,  0,  0,   5,  1,  0,  3,  0,   2],
    'domain_age_days': [5000, 5, 4000, 10, 3500, 2, 6000, 1, 15, 20, 4500, 5, 3000, 5000, 1, 12, 4000, 3, 5500, 8],
    'target':          [ 0,   1,  0,   1,  0,  1,  0,   1,  1,  1,  0,   1,  0,  0,   1,  1,  0,  1,  0,   1]
}

def create_dataset():
    df = pd.DataFrame(data)
    df.to_csv(CSV_PATH, index=False)
    print(f"[SUCCESS] Training dataset successfully generated at '{CSV_PATH}' with {len(df)} rows and {len(df.columns)} columns.")

if __name__ == "__main__":
    create_dataset()
