import streamlit as st
import sqlite3
import os
import pandas as pd





# -----------------------------
# Database Path
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# -----------------------------
# Load Global CSS
# -----------------------------
CSS_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "style.css"
)

if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Admin Dashboard | JobConnect AI",
    page_icon="🛡️",
    layout="wide"
)


# -----------------------------
# Admin Access Protection
# -----------------------------
if not st.session_state.get("admin_logged_in", False):
    st.error("Access denied. Admin login required.")
    st.stop()

# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)


# -----------------------------
# Get Users
# -----------------------------
def get_users():
    conn = get_connection()

    query = """
        SELECT id, name, email, role
        FROM users
        ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

# -----------------------------
# Update User Role
# -----------------------------
def update_user_role(user_id, new_role):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET role = ? WHERE id = ?",
        (new_role, user_id)
    )

    conn.commit()
    conn.close()

# -----------------------------
# Dashboard
# -----------------------------
admin_data = st.session_state.get("admin_data")
admin_name = admin_data[1] if admin_data else "Admin"

st.markdown(
    f"""
    <div class="admin-header">
        <h1>🛡️ Admin Dashboard</h1>
        <p>Welcome back, {admin_name}</p>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("Logout"):
    st.session_state.admin_logged_in = False
    st.session_state.admin_data = None

    st.rerun()

st.divider()

# -----------------------------
# Analytics
# -----------------------------
users_df = get_users()

total_users = len(users_df)
admin_users = len(users_df[users_df["role"] == "admin"])
regular_users = len(users_df[users_df["role"] == "user"])

st.markdown(
    '<div class="admin-section">📊 Project Analytics</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="admin-card">
            <div class="admin-card-title">Total Users</div>
            <div class="admin-card-value">{total_users}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="admin-card">
            <div class="admin-card-title">Regular Users</div>
            <div class="admin-card-value">{regular_users}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="admin-card">
            <div class="admin-card-title">Administrators</div>
            <div class="admin-card-value">{admin_users}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


# -----------------------------
# User Management
# -----------------------------

st.markdown(
    '<div class="admin-section">👥 User Management</div>',
    unsafe_allow_html=True
)

if users_df.empty:
    st.info("No users found.")

else:
    search = st.text_input(
        "Search users",
        placeholder="Search by name or email..."
    )

    role_filter = st.selectbox(
        "Filter by role",
        ["All Users", "Regular Users", "Administrators"]
    )

    filtered_users = users_df.copy()

# Search filter
if search:
    search_lower = search.lower()

    filtered_users = filtered_users[
        filtered_users["name"].str.lower().str.contains(
            search_lower,
            na=False
        )
        |
        filtered_users["email"].str.lower().str.contains(
            search_lower,
            na=False
        )
    ]

# Role filter
if role_filter == "Regular Users":
    filtered_users = filtered_users[
        filtered_users["role"] == "user"
    ]

elif role_filter == "Administrators":
    filtered_users = filtered_users[
        filtered_users["role"] == "admin"
    ]

st.dataframe(
    filtered_users,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.markdown(
    '<div class="admin-section">⚙️ Manage User Role</div>',
    unsafe_allow_html=True
)

user_options = users_df[
    ["id", "name", "email", "role"]
].copy()

selected_user = st.selectbox(
    "Select User",
    user_options["id"].tolist(),
    format_func=lambda user_id: (
        f"{user_options.loc[user_options['id'] == user_id, 'name'].iloc[0]} "
        f"— {user_options.loc[user_options['id'] == user_id, 'email'].iloc[0]} "
        f"(ID: {user_id})"
    )
)

selected_row = user_options[
    user_options["id"] == selected_user
].iloc[0]

st.write(
    f"Current role: **{selected_row['role']}**"
)

new_role = st.selectbox(
    "New Role",
    ["user", "admin"],
    index=0 if selected_row["role"] == "user" else 1
)

if st.button("Update Role", use_container_width=True):

    # Prevent removing the last admin
    if (
        selected_row["role"] == "admin"
        and new_role == "user"
        and admin_users <= 1
    ):
        st.warning(
            "You cannot remove the last administrator."
        )

    elif new_role == selected_row["role"]:
        st.info(
            "The selected user already has this role."
        )

    else:
        update_user_role(selected_user, new_role)

        st.success(
            f"Role updated successfully to '{new_role}'."
        )

        st.rerun()