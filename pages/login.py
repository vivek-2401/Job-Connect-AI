import streamlit as st
import sqlite3

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="Login | JobConnect AI",
    page_icon="🔐",
    layout="wide"
)

# ---------------- Load CSS ---------------- #

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- Layout ---------------- #

left, right = st.columns([1.2, 1], gap="large")

# ================= LEFT ================= #

with left:

    st.markdown(
        """
        <div class="auth-left">

        <div class="auth-logo">
        💼 JobConnect AI
        </div>

        <div class="auth-tagline">
        Your AI Career Partner
        </div>

        <div class="auth-desc">
        Upload your resume, discover live jobs,
        analyze your skills and receive
        AI-powered career guidance.
        </div>

        <div class="auth-feature">
        🤖 AI Career Assistant
        </div>

        <div class="auth-feature">
        📄 Resume Analysis
        </div>

        <div class="auth-feature">
        💼 Live Job Search
        </div>

        <div class="auth-feature">
        🎯 Resume Match Score
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

# ================= RIGHT ================= #

with right:

    st.markdown(
        """
        <div class="right-card">

        <h6>Welcome Back 👋</h6>

        <p>
        Login or create an account
        to continue your AI career journey.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter your password"
    )

    st.write("")

    if st.button("Login", use_container_width=True):

        if email == "" or password == "":
            st.error("Please fill all fields.")

        else:

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, password)
            )

            user = cursor.fetchone()

            conn.close()

            if user:
                st.session_state["user"] = user[1]
                st.switch_page("pages/dashboard.py")

            else:
                st.error("Invalid Email or Password")

    st.write("")

    if st.button("📝 Create New Account", use_container_width=True):
        st.switch_page("pages/register.py")

    st.markdown(
        """
        <div style="text-align:center;
                    margin-top:20px;
                    color:#64748B;">
        Secure • Fast • AI Powered
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )