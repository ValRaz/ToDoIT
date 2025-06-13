import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# ---- Firestore Initialization ----
cred = credentials.Certificate(
    r"C:\Users\nutca\Downloads\todo-it-109a2-firebase-adminsdk-fbsvc-f6afa6d121.json"
)
try:
    firebase_admin.initialize_app(cred, {
        'projectId': 'todo-it-109a2'
    })
except ValueError:
    pass

db = firestore.client()

# Creates a new task
def create_task(title: str, description: str = "") -> str:
    """
    Creates a new task in Firestore; returns the document ID.
    """
    now = datetime.now(timezone.utc)
    doc_ref = db.collection("tasks").document()
    doc_ref.set({
        "title": title,
        "description": description,
        "status": "pending",
        "created_at": now,
        "updated_at": now
    })
    return doc_ref.id

# Sets up page configuration
st.set_page_config(
    page_title="Cloud To-Do App",
    page_icon="\u2705",
    layout="wide",
)

st.title("\U0001F3F7\ufe0f ToDo*IT")
st.markdown(
    """
    A simple To-Do List app powered by Streamlit and Firestore.
    Add, view, update, and delete your personal tasks!
    """
)

st.sidebar.header("\U0001F50E Filters & Sorting")
status_filter = st.sidebar.selectbox("Status", ["all", "pending", "completed"])
sort_order    = st.sidebar.radio("Sort by", ["created_at", "updated_at"])

# Sets up container layout for the UI
col1, col2 = st.columns([2, 1])

with col1:
    # Sets up filtering on left sidebar
    st.markdown("### \U0001F4CB Task List")
    docs = db.collection("tasks").order_by(sort_order).stream()
    filtered = []
    for doc in docs:
        data = doc.to_dict()
        if status_filter == "all" or data["status"] == status_filter:
            filtered.append((doc.id, data))

    # Displays the filtered list
    for doc_id, data in filtered:
        checked = st.checkbox(
            data["title"],
            value=(data["status"] == "completed"),
            key=doc_id
        )
        if checked and data["status"] != "completed":
            db.collection("tasks").document(doc_id).update({
                "status": "completed",
                "updated_at": datetime.now(timezone.utc)
            })
        elif not checked and data["status"] != "pending":
            db.collection("tasks").document(doc_id).update({
                "status": "pending",
                "updated_at": datetime.now(timezone.utc)
            })

        # Delete button
        if st.button("\U0001F5D1\ufe0f Delete", key=f"del-{doc_id}"):
            db.collection("tasks").document(doc_id).delete()
            st.experimental_rerun()

# Displays the create task form
with col2:
    st.markdown("### \U0001F4DD Add a New Task")
    with st.form("create_task_form"):
        new_title = st.text_input("Title")
        new_desc  = st.text_area("Description")
        submitted = st.form_submit_button("Create Task")

        if submitted:
            if not new_title.strip():
                st.error("Title cannot be empty.")
            else:
                create_task(new_title, new_desc)
                st.success("\u2705 Task created successfully!")

# Footer
st.markdown("---")
st.write("\u00A9 2025 Valerie Rasmussen, Built with \u2764\ufe0f using Streamlit and Firestore")