import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from phishguard.api.app import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("phishguard.api.app:app", host="127.0.0.1", port=8000, reload=True)
