import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
from streamlit_autorefresh import st_autorefresh

# Initializes Firestore
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

# Enables polling to auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="polling")

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

# Sets up create-form counter for clearing
if "create_counter" not in st.session_state:
    st.session_state["create_counter"] = 0

with col2:
    # Displays the create task form
    st.markdown("### \U0001F4DD Add a New Task")
    form_key = f"create_task_form_{st.session_state['create_counter']}"
    with st.form(form_key):
        new_title = st.text_input("Title", key="new_title")
        new_desc  = st.text_area("Description", key="new_desc")
        submitted = st.form_submit_button("Create Task")

        if submitted:
            if not new_title.strip():
                st.error("Title cannot be empty.")
            else:
                create_task(new_title, new_desc)
                st.session_state["create_counter"] += 1
                st.success("\u2705 Task created!")

with col1:
    # Displays the filtered list
    st.markdown("### \U0001F4CB Task List")
    docs = db.collection("tasks").order_by(sort_order).stream()

    for doc in docs:
        data = doc.to_dict()
        if status_filter != "all" and data["status"] != status_filter:
            continue

        # Title & description
        st.markdown(f"**{data['title']}**")
        st.write(data["description"])

        # Completion toggle
        checked = st.checkbox(
            "Mark complete",
            value=(data["status"] == "completed"),
            key=f"chk-{doc.id}",
            label_visibility="hidden"
        )
        if checked and data["status"] != "completed":
            db.collection("tasks").document(doc.id).update({
                "status": "completed",
                "updated_at": datetime.now(timezone.utc)
            })
        elif not checked and data["status"] != "pending":
            db.collection("tasks").document(doc.id).update({
                "status": "pending",
                "updated_at": datetime.now(timezone.utc)
            })

        # Delete button
        if st.button("\U0001F5D1\ufe0f Delete", key=f"del-{doc.id}"):
            db.collection("tasks").document(doc.id).delete()

        # Sets up edit-form counter for clearing
        edit_counter_key = f"edit_counter_{doc.id}"
        if edit_counter_key not in st.session_state:
            st.session_state[edit_counter_key] = 0

        # Compute dynamic keys using the counter
        title_key = f"edit_title_{doc.id}_{st.session_state[edit_counter_key]}"
        desc_key  = f"edit_desc_{doc.id}_{st.session_state[edit_counter_key]}"
        form_key  = f"edit_form_{doc.id}_{st.session_state[edit_counter_key]}"

        # Edit task expander
        with st.expander("\u270F\ufe0f Edit Task", expanded=False):
            with st.form(form_key):
                edit_title = st.text_input("Title", value="", key=title_key)
                edit_desc  = st.text_area("Description", value="", key=desc_key)

                save = st.form_submit_button("Save Changes")

                if save:
                    db.collection("tasks").document(doc.id).update({
                        "title": edit_title,
                        "description": edit_desc,
                        "updated_at": datetime.now(timezone.utc)
                    })
                    # Force fields to reset by incrementing counter
                    st.session_state[edit_counter_key] += 1
                    st.success("\u2705 Task updated!")

# Footer
st.markdown("---")
st.write("\u00A9 2025 Valerie Rasmussen, Built with \u2764\ufe0f using Streamlit and Firestore")