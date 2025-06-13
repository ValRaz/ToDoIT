import os, sys
import pytest
import requests

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"

# Base URL for Firestore emulator’s REST API
PROJECT_ID = "todo-it-109a2"
BASE_URL = f"http://{os.environ['FIRESTORE_EMULATOR_HOST']}/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# REST WRL build helper
def url(path: str) -> str:
    return f"{BASE_URL}{path}"

# Tests unauthenticated read attempt
def test_unauthenticated_get():
    resp = requests.get(url("/tasks"))
    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}"

# Tests unauthenticated create attempt
def test_unauthenticated_create():
    """
    POST to /tasks should be forbidden without auth or correct ownerId.
    """
    payload = {
        "fields": {
            "title":       {"stringValue": "foo"},
            "description": {"stringValue": "bar"},
            "status":      {"stringValue": "pending"},
            "ownerId":     {"stringValue": "not-your-uid"}
        }
    }
    resp = requests.post(url("/tasks"), json=payload)
    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}"
