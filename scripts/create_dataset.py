from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "phishing_data.csv"

DATA = {
    "url_length": [15, 80, 22, 110, 18, 95, 25, 120, 60, 55, 12, 115, 70, 20, 150, 45, 30, 85, 14, 105],
    "has_at_symbol": [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    "has_https": [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    "no_of_dots": [1, 5, 1, 4, 2, 6, 1, 5, 2, 3, 1, 6, 2, 1, 8, 2, 1, 4, 1, 5],
    "has_ip": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    "hyphen_count": [0, 3, 0, 4, 0, 2, 0, 3, 1, 2, 0, 4, 0, 0, 5, 1, 0, 3, 0, 2],
    "domain_age_days": [5000, 5, 4000, 10, 3500, 2, 6000, 1, 15, 20, 4500, 5, 3000, 5000, 1, 12, 4000, 3, 5500, 8],
    "target": [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
}


def create_dataset() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(DATA).to_csv(DATA_PATH, index=False)
    print(f"[SUCCESS] Dataset written to '{DATA_PATH}'")


if __name__ == "__main__":
    create_dataset()
