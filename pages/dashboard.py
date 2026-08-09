import streamlit as st

from api import search_jobs
from utils.resume_parser import (
    parse_resume,
    extract_skills,
    calculate_resume_score
)

from utils.career_analysis import analyze_resume

# ------------------ Page Config ------------------

st.set_page_config(
    page_title="JobConnect AI",
    page_icon="💼",
    layout="wide"
)


# ------------------ Load CSS ------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# ------------------ Login Check ------------------

if "user" not in st.session_state:
    st.warning("Please Login First")
    st.switch_page("pages/login.py")


# ------------------ Header ------------------

st.title("💼 JobConnect AI")

st.caption(
    f"Welcome, **{st.session_state['user']}** 👋"
)

st.divider()


# ------------------ Resume Upload ------------------

with st.container(border=True):

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose your Resume (PDF)",
        type=["pdf"]
    )


# ------------------ Resume Processing ------------------

if uploaded_file is not None:

    resume_text = parse_resume(uploaded_file)

    st.session_state["resume_text"] = resume_text


    # ---------------- Skills ----------------

    found_skills = extract_skills(resume_text)


    # ---------------- Resume Score ----------------

    score = calculate_resume_score(found_skills)


    # ------------------ AI Career Analysis ------------------

career_data = {
    "job_roles": [],
    "missing_skills": []
}

with st.spinner("🤖 Analyzing your career profile..."):

    try:
        print("DEBUG resume_text type:", type(resume_text))
        print("DEBUG resume_text length:", len(resume_text))

        career_data = analyze_resume(resume_text)

        print("DEBUG career_data:", career_data)

    except Exception as e:
        print("Career Analysis Error:", repr(e))


job_roles = career_data.get("job_roles", [])
ai_missing_skills = career_data.get("missing_skills", [])

print("ALL JOB ROLES:", job_roles)
print("TOTAL JOB ROLES:", len(job_roles))

# ------------------ Live Jobs ------------------

jobs = []

if job_roles:

    with st.spinner("🔍 Searching Live Jobs..."):

        try:

            all_jobs = []

            for role in job_roles:

                role_jobs = search_jobs(role)


                if role_jobs:
                    all_jobs.extend(role_jobs)

            # Remove duplicate jobs
            seen_jobs = set()

            for job in all_jobs:

                if not isinstance(job, dict):
                    continue

                job_id = (
                    job.get("job_id")
                    or job.get("job_apply_link")
                    or job.get("job_google_link")
                    or job.get("job_title")
                )

                if job_id and job_id not in seen_jobs:

                    seen_jobs.add(job_id)
                    jobs.append(job)

        except Exception as e:

            print("Job Search Error:", e)

            jobs = []
    # ---------------- Dashboard Cards ----------------

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Resume Score",
            f"{score}/10"
        )

    with col2:
        st.metric(
            "Skills Found",
            len(found_skills)
        )

    with col3:
        st.metric(
            "Jobs Found",
            len(jobs)
        )


    st.divider()


    # ---------------- Resume ----------------

    with st.expander("📄 View Resume"):

        st.text_area(
            "Resume",
            resume_text,
            height=220
        )


    # ---------------- Skills ----------------

    st.subheader("🛠 Skills Found")

    if found_skills:

        cols = st.columns(4)

        for i, skill in enumerate(found_skills):

            cols[i % 4].success(skill)

    else:

        st.warning("No Skills Found")


    st.divider()

    # ---------------- Suggested Skills ----------------

    st.subheader("📚 Suggested Skills")

    missing_skills = ai_missing_skills

    if missing_skills:

        cols = st.columns(3)

        for i, skill in enumerate(missing_skills):

            cols[i % 3].info(skill)

    else:

        st.success(
            "🎉 No major additional skills were identified."
        )


    # ---------------- Recommended Job Roles ----------------

    st.subheader("🎯 Recommended Job Roles")

    if job_roles:

        cols = st.columns(3)

        for i, role in enumerate(job_roles):

            cols[i % 3].success(role)

    else:

        st.info(
            "No suitable job roles identified from your resume."
        )


    st.divider()
    # ---------------- Live Job Recommendations ----------------

    st.subheader("💼 Live Job Recommendations")


    if jobs:

        for job in jobs:

            with st.container(border=True):

                st.markdown(
                    f"### 💼 {job.get('job_title', 'N/A')}"
                )

                col1, col2 = st.columns([4, 1])


                with col1:

                    st.write(
                        f"**🏢 Company:** "
                        f"{job.get('employer_name', 'N/A')}"
                    )

                    city = (
                        job.get("job_city")
                        or "Not Mentioned"
                    )

                    country = (
                        job.get("job_country")
                        or ""
                    )

                    st.write(
                        f"**📍 Location:** "
                        f"{city}, {country}"
                    )

                    st.write(
                        f"**💻 Employment:** "
                        f"{job.get('job_employment_type', 'N/A')}"
                    )

                    salary = (
                        job.get("job_salary_string")
                        or job.get("job_salary")
                        or "Not Mentioned"
                    )

                    st.write(
                        f"**💰 Salary:** {salary}"
                    )


                with col2:

                    apply_link = (
                        job.get("job_apply_link")
                        or job.get("job_google_link")
                    )

                    if apply_link:

                        st.link_button(
                            "🚀 Apply",
                            apply_link,
                            use_container_width=True
                        )

                    else:

                        st.button(
                            "Not Available",
                            disabled=True,
                            use_container_width=True
                        )


    else:

        st.info(
            "No Live Jobs Found. "
            "Please try again when the job search service is available."
        )


# ---------------- Sidebar ----------------

with st.sidebar:

    st.title("💼 JobConnect AI")

    st.write("👋 Welcome")

    st.success(
        st.session_state["user"]
    )

    st.divider()

    st.page_link(
        "pages/ai_assistant.py",
        label="🤖 AI Assistant"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        del st.session_state["user"]

        st.switch_page("pages/login.py")