import streamlit as st
import sqlite3

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="Register | JobConnect AI",
    page_icon="📝",
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
        Start Your AI Career Journey
        </div>

        <div class="auth-desc">
        Create your account and unlock AI-powered
        resume analysis, live job search,
        resume matching and career guidance.
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

    name = st.text_input(
        "👤 Full Name",
        placeholder="Enter your full name"
    )

    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Create a password"
    )

    st.write("")

    if st.button("Register", use_container_width=True):

        if name == "" or email == "" or password == "":
            st.error("Please fill all fields.")

        else:

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )

            conn.commit()
            conn.close()

            st.success("🎉 Registration Successful!")

    st.write("")

    if st.button("🔐 Already have an account?", use_container_width=True):
        st.switch_page("pages/login.py")

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