from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import os
import sys

# Ensure container can import local modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Create FastAPI app with proper agent loading
app: FastAPI = get_fast_api_app(
    agents_dir=".",  # Look in current directory
    web=True
)