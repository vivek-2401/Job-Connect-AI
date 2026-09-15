import streamlit as st
import sqlite3
import os


# -----------------------------
# Database Path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "users.db")


# -----------------------------
# Admin Authentication
# -----------------------------
def admin_login(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email, role
        FROM users
        WHERE email = ?
        AND password = ?
        AND role = 'admin'
        """,
        (email, password)
    )

    admin = cursor.fetchone()
    conn.close()

    return admin


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Admin Login | JobConnect AI",
    page_icon="🔐",
    layout="centered"
)


# -----------------------------
# Session State
# -----------------------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "admin_data" not in st.session_state:
    st.session_state.admin_data = None


# -----------------------------
# Already Logged In
# -----------------------------
if st.session_state.admin_logged_in:
    st.success("Admin already logged in.")

    if st.button("Go to Admin Dashboard"):
        st.switch_page("pages/admin_dashboard.py")

    st.stop()
# -----------------------------
# Admin Login UI
# -----------------------------
st.title("🔐 JobConnect AI")
st.subheader("Admin Login")

st.write("Login with your administrator account.")

email = st.text_input(
    "Admin Email",
    placeholder="Enter admin email"
)

password = st.text_input(
    "Admin Password",
    type="password",
    placeholder="Enter admin password"
)


# -----------------------------
# Login Button
# -----------------------------
if st.button("Login as Admin", use_container_width=True):

    if not email or not password:
        st.warning("Please enter both email and password.")

    else:
        admin = admin_login(email, password)

        if admin:
            st.session_state.admin_logged_in = True
            st.session_state.admin_data = admin

            st.success("Admin login successful!")

            st.switch_page("pages/admin_dashboard.py")
        else:
            st.error("Invalid admin credentials.")