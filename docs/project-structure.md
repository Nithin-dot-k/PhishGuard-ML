# Project Structure

This document explains the purpose of each tracked project file and directory.

## Root Files

| Path               | Responsibility                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `README.md`        | Public project overview, setup instructions, usage, and limitations.                                               |
| `pyproject.toml`   | Python package metadata plus pytest and Ruff configuration.                                                        |
| `requirements.txt` | Runtime, dashboard, ML, HTTP, and test dependencies.                                                               |
| `.env.example`     | Placeholder for environment-specific configuration documentation. It contains no secrets.                          |
| `.gitignore`       | Excludes virtual environments, caches, local environment files, and generated Python metadata.                     |
| `main.py`          | Compatibility launcher for the local FastAPI application. It adds `src/` to the import path and exposes `app`.     |
| `app.py`           | Compatibility launcher for the Streamlit dashboard. The implementation lives in `src/phishguard/dashboard/app.py`. |
| `vercel.json`      | Routes Vercel requests to `api/main.py`.                                                                           |

## Application Package

The application package is under `src/phishguard/`. Keeping application code here prevents accidental imports from unrelated repository files and supports standard Python packaging.

| Path                                   | Responsibility                                                                                                  |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `src/phishguard/__init__.py`           | Marks `phishguard` as a Python package.                                                                         |
| `src/phishguard/feature_extractor.py`  | Parses URLs and produces the seven model input features. WHOIS lookups are optional and fail closed to age `0`. |
| `src/phishguard/heuristic_engine.py`   | Applies the trusted-domain allowlist, brand-spoof rules, risk adjustments, and verdict labels.                  |
| `src/phishguard/predictor.py`          | Locates and caches the trained model, runs feature extraction and prediction, then builds the API result.       |
| `src/phishguard/api/__init__.py`       | Marks the API module as a package.                                                                              |
| `src/phishguard/api/app.py`            | Creates the FastAPI application, configures CORS, defines health/root routes, and exposes analysis routes.      |
| `src/phishguard/api/schemas.py`        | Defines the Pydantic request schema for URL analysis.                                                           |
| `src/phishguard/dashboard/__init__.py` | Marks the dashboard module as a package.                                                                        |
| `src/phishguard/dashboard/app.py`      | Implements the Streamlit user interface for submitting URLs and viewing analysis results.                       |

## API Deployment Adapter

| Path                     | Responsibility                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| `api/main.py`            | Vercel-compatible adapter that imports the shared FastAPI application from `phishguard.api.app`. |
| `api/phishing_model.pkl` | Deployment copy of the generated model artifact used by the serverless environment.              |
| `api/requirements.txt`   | Dependency manifest used by the Vercel Python deployment.                                        |

The API adapter should remain thin. Business logic belongs in `src/phishguard/`, so local and serverless execution use the same application behavior.

## Data and Model Artifacts

| Path                         | Responsibility                                                                                                 |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `data/raw/phishing_data.csv` | Canonical training dataset containing feature columns and the `target` label.                                  |
| `data/create_dataset.py`     | Retained historical dataset-generation script. New work should use `scripts/create_dataset.py`.                |
| `models/phishing_model.pkl`  | Local generated Random Forest model artifact.                                                                  |
| `models/train_model.py`      | Retained historical training script. New work should use `scripts/train_model.py`.                             |
| `models/README.md`           | Notes describing how model artifacts are generated and copied.                                                 |
| `scripts/create_dataset.py`  | Canonical dataset-generation command. Writes `data/raw/phishing_data.csv`.                                     |
| `scripts/train_model.py`     | Canonical training command. Reads the dataset, trains the model, and copies artifacts to `models/` and `api/`. |

The `.pkl` files are generated outputs. They should be regenerated through the training script rather than edited manually.

## Browser Extension

| Path                      | Responsibility                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| `extension/manifest.json` | Chrome Manifest V3 metadata, permissions, and popup registration.                          |
| `extension/popup.html`    | Popup markup shown when the extension icon is selected.                                    |
| `extension/popup.js`      | Reads the active tab URL, calls the configured API endpoints, and renders the risk result. |
| `extension/icon.png`      | Browser extension icon asset.                                                              |

## Tests and Automation

| Path                       | Responsibility                                                                                                  |
| -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `tests/test_features.py`   | Tests IP detection, feature extraction, dataframe columns, allowlisting, brand spoofing, and heuristic results. |
| `tests/test_api.py`        | Tests the root, health, safe URL, and phishing URL API behavior.                                                |
| `.github/workflows/ci.yml` | Installs Python dependencies and runs pytest for pushes and pull requests.                                      |

## Directory Ownership Rules

- Put reusable application behavior in `src/phishguard/`.
- Put one-off data and model commands in `scripts/`.
- Keep deployment adapters such as `api/main.py` thin.
- Keep generated data and model artifacts out of handwritten application modules.
- Add or update tests when changing a public API route or detection rule.
