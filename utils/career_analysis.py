import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()


# ------------------ Gemini Client ------------------

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# ------------------ Resume Analysis ------------------

def analyze_resume(resume_text):

    """
    Analyze resume and identify suitable job roles
    and missing skills for any career field.
    """

    prompt = f"""
You are JobConnect AI, an expert career advisor.

Analyze the following resume:

---------------- RESUME ----------------

{resume_text}

------------------------------------------

Return ONLY valid JSON in this format:

{{
    "job_roles": [
        "role 1",
        "role 2",
        "role 3"
    ],
    "missing_skills": [
        "skill 1",
        "skill 2",
        "skill 3"
    ]
}}

Rules:

- Do NOT assume the person is a software developer.
- Support ANY career field.
- Examples include:
  IT, Data, Finance, Accounting, HR,
  Marketing, Sales, Teaching, Healthcare,
  Design, Engineering, Legal and others.
- Select job roles that actually match the resume.
- Give exactly 3 suitable job roles.
- Give up to 5 useful missing skills.
- Do not suggest unrelated skills.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown code block if Gemini adds it

        if text.startswith("```"):

            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        result = json.loads(text)

        return {
            "job_roles": result.get("job_roles", []),
            "missing_skills": result.get("missing_skills", [])
        }

    except Exception as e:

        print("Career Analysis Error:", e)

        return {
            "job_roles": [],
            "missing_skills": []
        }