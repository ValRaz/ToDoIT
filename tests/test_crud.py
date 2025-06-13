import os, sys
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import app

@pytest.fixture(scope="module")
def client():
    cred = credentials.ApplicationDefault()
    try:
        firebase_admin.initialize_app(cred, {"projectId": "todo-it-109a2"})
    except ValueError:
        pass
    emu_client = firestore.client()
    app.db = emu_client
    return emu_client

# Tests task create and read functionality
def test_create_and_read_task(client):
    title = "PyTest Task"
    desc  = "Created in unit test"
    new_id = app.create_task(title, desc)
    doc = client.collection("tasks").document(new_id).get()
    data = doc.to_dict()
    assert data["title"] == title
    assert data["description"] == desc
    assert data["status"] == "pending"
    assert hasattr(data["created_at"], "timestamp")
    assert hasattr(data["updated_at"], "timestamp")

# Tests task status update functionality
def test_update_task_status(client):
    tid = app.create_task("ToUpdate", "")
    client.collection("tasks").document(tid).update({"status": "completed"})
    doc = client.collection("tasks").document(tid).get()
    assert doc.to_dict()["status"] == "completed"

# Tests delete task functionality
def test_delete_task(client):
    tid = app.create_task("ToDelete", "")
    client.collection("tasks").document(tid).delete()
    doc = client.collection("tasks").document(tid).get()
    assert not doc.exists