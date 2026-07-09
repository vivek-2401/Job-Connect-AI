import streamlit as st

st.set_page_config(
    page_title="Job Connect AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Job Connect AI")

st.subheader("AI Powered Career Assistant")

st.write("""
Welcome to **Job Connect AI** 🚀

This platform helps job seekers to:

✅ Upload Resume

✅ Get ATS Score

✅ Search Jobs

✅ AI Career Guidance

✅ Company Information

✅ Smart Job Recommendations
""")

if st.button("🚀 Get Started"):
    st.success("Welcome to Job Connect AI")