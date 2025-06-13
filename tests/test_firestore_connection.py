import pytest
import firebase_admin
from firebase_admin import credentials, firestore

@pytest.fixture(scope = "module")
# Initializes Firestore
def db_client():
    cred = credentials.Certificate(r"C:\Users\nutca\Downloads\todo-it-109a2-firebase-adminsdk-fbsvc-f6afa6d121.json")
    try:
        firebase_admin.initialize_app(cred)
    except ValueError:
        pass
    return firestore.client()

# Smoke test for Firestore access to tasks collection
def test_connection(db_client):
    try:
        docs = db_client.collection("tasks").get()
    except Exception as e:
        pytest.fail(f"Failed to read from Firestore: {e}")
    assert hasattr(docs, "__iter__"), "Expected iterable of documents"

# Checks for non negative task count
def test_task_count(db_client):
    docs = db_client.collection("tasks").get()
    count = len(docs)
    assert count >= 0, f"Task count should not be negative (got {count})"