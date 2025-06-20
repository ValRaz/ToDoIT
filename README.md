# Overview
For this project, I set out to build a simple yet powerful To-Do List application that leverages a managed NoSQL database. This project demonstrates how to integrate a Streamlit-based Python frontend with Google Cloud Firestore, enabling real-time-like CRUD operations, structured data modeling, and secure client-side interactions. This application allows users to **create**, **read**, **update**, and **delete** personal tasks through an intuitive web interface.
My goal in writing this software is to deepen my understanding of cloud database modeling, serverless API integration, and reactive web interfaces. By end-to-end developing this app, I’ve reinforced best practices for data schema design, local testing against the Firestore emulator, and continuous UI refresh techniques.

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database
I used **Google Cloud Firestore** as the backend database for its serverless scalability, real-time listeners, and fine-grained security rules.

- **Project ID**: `todo-it-109a2`
- **Mode**: Native mode Firestore (NoSQL document store)

## Structure
- **Collection**: `tasks`
  Each document represents a single to-do item, with the following fields:
  - `title` (string): The task’s name
  - `description` (string): Detailed notes about the task
  - `status` (string): Either `"pending"` or `"completed"`
  - `created_at` (timestamp): UTC timestamp when the task was first created
  - `updated_at` (timestamp): UTC timestamp of the last modification

Indexes are automatically handled for single-field ordering (e.g., ordering by `created_at` or `updated_at`). Composite indexes can be added via the Firebase console as needed for advanced queries.

# Development Environment
- **Language**: Python 3.11+
- **Framework**: Streamlit for rapid UI development
- **Firebase Admin SDK**: `firebase-admin` Python package for server-side Firestore operations
- **Firestore Emulator**: Local emulator for unit testing CRUD operations without hitting production
- **Additional Libraries**:
  - `streamlit-autorefresh` for polling-based live updates
  - `pytest` for writing and running unit tests
  - `python-dotenv` (optional) for managing environment variables

Development was done in VS Code on Windows, using a virtual environment (`venv`) to isolate dependencies.

# Useful Websites
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Firebase Firestore Docs](https://firebase.google.com/docs/firestore)
- [Firestore Emulator Guide](https://firebase.google.com/docs/emulator-suite)
- [pytest Documentation](https://docs.pytest.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

# Future Work
- Add **user authentication** so each user sees only their own tasks
- Implement **Firestore Security Rules** to enforce per-user data access
- Enhance UI with **drag-and-drop ordering**, due-date calendar view, and notifications