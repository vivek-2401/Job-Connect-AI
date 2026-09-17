import sqlite3
import os
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


# -----------------------------
# Database Path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")


# -----------------------------
# Database Setup
# -----------------------------
def initialize_database():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    # Check old database
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "role" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'"
        )

    # -----------------------------
    # Create Admin from Secrets
    # -----------------------------
    try:
        admin_email = st.secrets.get("ADMIN_EMAIL")
        admin_password = st.secrets.get("ADMIN_PASSWORD")

    except StreamlitSecretNotFoundError:
        admin_email = None
        admin_password = None

    if admin_email and admin_password:

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (admin_email,)
        )

        existing_admin = cursor.fetchone()

        if existing_admin:
            cursor.execute(
                "UPDATE users SET role = 'admin' WHERE email = ?",
                (admin_email,)
            )

        else:
            cursor.execute(
                """
                INSERT INTO users
                (name, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    "Administrator",
                    admin_email,
                    admin_password,
                    "admin"
                )
            )

    conn.commit()
    conn.close()


# -----------------------------
# Initialize Database
# -----------------------------
initialize_database()