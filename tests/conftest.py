"""
Common fixtures that:
* stub Google Cloud dependencies so tests run offline
* prime environment variables ADK expects
"""
import os, google.auth
import pytest
import sys, pathlib
from unittest import mock


ROOT     = pathlib.Path(__file__).resolve().parents[1]  # project root
SRC_PATH = ROOT / "src"                                 # /src
sys.path.insert(0, str(SRC_PATH))                       # ← key line

# Stub google.auth.default globally so *every* import sees it
google.auth.default = lambda *a, **k: (None, "test-project")

# Pre-seed env so root_agent doesn’t have to
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

@pytest.fixture(autouse=True)
def _patch_google(monkeypatch):
    # Fake ADC → returns (credentials, project_id)
    monkeypatch.setattr(
        "google.auth.default", lambda *a, **k: (None, "test-project")
    )

    # Fake Cloud Logging so .logger() & .log_text() don’t hit the network
    dummy_logger = mock.Mock(log_text=lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "google.cloud.logging.Client",
        lambda *a, **k: mock.Mock(logger=lambda *_: dummy_logger),
    )

    # Minimal env so ADK initialisation doesn’t explode
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
