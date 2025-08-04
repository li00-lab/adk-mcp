# server.py  (minimal change)

from pathlib import Path
import sys
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

BASE_DIR   = Path(__file__).resolve().parent      # /adk-mcp
AGENTS_DIR = BASE_DIR / "src"                 # /adk-mcp/agents

# Let `import agents.foo` work everywhere in the project
sys.path.insert(0, str(AGENTS_DIR))

app: FastAPI = get_fast_api_app(
    agents_dir=str(AGENTS_DIR),  # ✅ only this folder is crawled
    web=True                     # keep the rest of your kwargs
)
