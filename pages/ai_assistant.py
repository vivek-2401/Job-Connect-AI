import streamlit as st

from utils.ai_match import ai_match
from utils.memory import initialize_chat, add_message, get_messages
from utils.ai import ask_ai
from utils.intent import is_job_search
from utils.rag import index_resume
from api import search_jobs


# ------------------ Page Config ------------------

st.set_page_config(
    page_title="JobConnect AI - AI Assistant",
    page_icon="🤖",
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


# ------------------ Title ------------------

st.title("🤖 AI Job Assistant")

st.caption(
    "Ask questions about your resume, career, skills and jobs."
)

st.divider()


# ------------------ Sidebar ------------------

with st.sidebar:

    st.title("💼 JobConnect AI")

    st.write("👋 Welcome")

    st.success(st.session_state["user"])

    st.divider()

    st.page_link(
        "pages/dashboard.py",
        label="🏠 Dashboard"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        # Clear chat history
        st.session_state.pop("messages", None)

        # Clear resume-related session data
        st.session_state.pop("resume_text", None)
        st.session_state.pop("resume_indexed", None)


        # Clear logged-in user
        st.session_state.pop("user", None)

        st.switch_page("pages/login.py")


# ------------------ Chat Memory ------------------

initialize_chat()


# ------------------ Display Previous Messages ------------------

for message in get_messages():

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ------------------ Chat Input ------------------

prompt = st.chat_input(
    "Ask anything about your career..."
)


# ------------------ Process Message ------------------

if prompt:

    # User message
    add_message(
        "user",
        prompt
    )

    with st.chat_message("user"):

        st.markdown(prompt)


    # ------------------ Resume ------------------

    resume = st.session_state.get(
        "resume_text",
        ""
    )


    # ------------------ Index Resume ------------------

    if resume and not st.session_state.get(
        "resume_indexed",
        False
    ):

        index_resume(resume)

        st.session_state["resume_indexed"] = True


    # ------------------ Job Search ------------------

    if is_job_search(prompt):

        with st.chat_message("assistant"):

            with st.spinner(
                "🔍 Searching Live Jobs..."
            ):

                jobs = search_jobs(prompt)


            if jobs:

                response_text = (
                    f"Found {len(jobs)} matching jobs."
                )

                add_message(
                    "assistant",
                    response_text
                )

                st.success(
                    f"Found {len(jobs)} Jobs"
                )


                for job in jobs[:5]:

                    st.markdown(
                        f"### 💼 {job.get('job_title', 'N/A')}"
                    )


                    st.write(
                        "🏢 Company:",
                        job.get(
                            "employer_name",
                            "N/A"
                        )
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
                        f"📍 Location: "
                        f"{city}, {country}"
                    )


                    st.write(
                        "💻 Employment:",
                        job.get(
                            "job_employment_type",
                            "N/A"
                        )
                    )


                    salary = (
                        job.get("job_salary_string")
                        or job.get("job_salary")
                        or "Not Mentioned"
                    )


                    st.write(
                        "💰 Salary:",
                        salary
                    )


                    # ------------------ AI Resume Match ------------------

                    result = ai_match(job)


                    st.progress(
                        result["match_score"]
                    )


                    st.write(
                        f"🎯 Resume Match: "
                        f"{result['match_score']}%"
                    )


                    st.success(
                        "✅ Matching Skills: "
                        + ", ".join(
                            result["matching_skills"]
                        )
                    )


                    st.warning(
                        "❌ Missing Skills: "
                        + ", ".join(
                            result["missing_skills"]
                        )
                    )


                    st.info(
                        "💪 Strengths:\n\n"
                        + "\n".join(
                            result["strengths"]
                        )
                    )


                    st.info(
                        "📚 Suggestions:\n\n"
                        + "\n".join(
                            result["suggestions"]
                        )
                    )


                    apply_link = (
                        job.get("job_apply_link")
                        or job.get("job_google_link")
                    )


                    if apply_link:

                        st.link_button(
                            "🚀 Apply Now",
                            apply_link,
                            use_container_width=True
                        )


            else:

                st.warning(
                    "No jobs found."
                )

                add_message(
                    "assistant",
                    "No jobs found."
                )


    # ------------------ Normal AI Chat ------------------

    else:

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Thinking..."
            ):

                response = ask_ai(
                    prompt,
                    resume
                )


            st.markdown(response)


            add_message(
                "assistant",
                response
            )