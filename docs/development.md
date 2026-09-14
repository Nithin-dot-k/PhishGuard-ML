# Development Guide

## Install Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Generate Data and Train

Use the canonical scripts:

```powershell
python scripts/create_dataset.py
python scripts/train_model.py
```

Expected artifacts:

- `data/raw/phishing_data.csv`
- `models/phishing_model.pkl`
- `api/phishing_model.pkl`

## Start the API

```powershell
python main.py
```

Useful endpoints:

- `GET http://127.0.0.1:8000/`
- `GET http://127.0.0.1:8000/health`
- `POST http://127.0.0.1:8000/api/analyze`
- `GET http://127.0.0.1:8000/docs`

Example request:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/api/analyze `
  -Method Post `
  -ContentType 'application/json' `
  -Body '{"url":"https://example.com","enable_whois":false}'
```

## Start the Dashboard

```powershell
streamlit run app.py
```

## Run the Browser Extension

1. Start the local API if the extension should use the local fallback.
2. Open `chrome://extensions`.
3. Enable **Developer mode**.
4. Select **Load unpacked**.
5. Choose the repository's `extension/` directory.

## Run Tests

```powershell
python -m pytest
```

Run syntax validation:

```powershell
python -m compileall -q src scripts main.py app.py api/main.py
```

## Add or Change a Detection Rule

1. Update the relevant function in `src/phishguard/heuristic_engine.py`.
2. Add a focused test in `tests/test_features.py`.
3. Run `python -m pytest tests/test_features.py`.
4. Run the complete suite with `python -m pytest`.
5. Update the API or architecture documentation if the response contract changes.

## Add or Change a Model Feature

1. Update `FEATURE_COLUMNS` and feature extraction in `src/phishguard/feature_extractor.py`.
2. Update the dataset schema in `scripts/create_dataset.py`.
3. Retrain with `python scripts/train_model.py`.
4. Update the feature list in `docs/architecture.md`.
5. Add or update feature tests.

Feature names and order must match between dataset creation, training, and inference.

## Deploy to Vercel

After training the intended model artifact:

```powershell
vercel deploy
```

Vercel uses `vercel.json` and `api/main.py`. The serverless path disables WHOIS lookups for predictable request behavior.

## CI

The workflow at `.github/workflows/ci.yml` runs on pushes and pull requests. It installs `requirements.txt` and executes `python -m pytest`.
