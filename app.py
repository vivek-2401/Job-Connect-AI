import streamlit as st

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="JobConnect AI",
    page_icon="💼",
    layout="wide"
)

# ---------------- Load CSS ---------------- #

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- Layout ---------------- #

left, right = st.columns([1, 1], gap="Medium")

# ================= LEFT ================= #

with left:

    st.markdown(
        """
        <div class="hero-title">
            💼 JobConnect AI
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Your AI Career Partner
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-text">
        Find your dream job with Artificial Intelligence.<br>
        Upload your resume, analyze your skills,
        search live jobs and receive AI-powered
        career guidance.
        </div>
        """,
        unsafe_allow_html=True,
    )

    features = [
        ("🤖", "AI Career Assistant"),
        ("📄", "Resume Analysis"),
        ("💼", "Live Job Search"),
        ("🎯", "Resume Match Score"),
    ]

    for icon, title in features:
        st.markdown(
            f"""
            <div class="feature-card">
                <h4>{icon} {title}</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ================= RIGHT ================= #

with right:

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="right-card">

        <h5>Welcome Back 👋</h5>

        <p>
        Login or create an account
        to continue your AI career journey.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/login.py")

    st.write("")

    if st.button("📝 Register", use_container_width=True):
        st.switch_page("pages/register.py")

    st.markdown(
        """
        <div style="text-align:center;
                    color:#64748B;
                    margin-top:18px;">
        Secure • Fast • AI Powered
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- Footer ---------------- #

st.markdown("<br><hr>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
    © 2026 JobConnect AI | AI Powered Career Platform
    </div>
    """,
    unsafe_allow_html=True,
)