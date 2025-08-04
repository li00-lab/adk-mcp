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
    import google.auth
    monkeypatch.setattr(google.auth, "default", lambda *a, **k: (None, "test-project"))

    # patch GCP logging client
    dummy_logger = mock.Mock(log_text=lambda *a, **k: None)
    monkeypatch.setattr(
        "google.cloud.logging.Client",
        lambda *a, **k: mock.Mock(logger=lambda *_: dummy_logger)
    )

    # basic env stub
    import os
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "test-project")
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")