import os
import json
from dotenv import load_dotenv
from google import genai

from utils.rag import retrieve_context

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def ai_match(job):

    context = retrieve_context(
        job.get("job_description", "")
    )

    prompt = f"""
    You are an expert ATS Resume Analyzer.

    Resume:
    {context}

    Job Title:
    {job.get("job_title", "")}

    Job Description:
    {job.get("job_description", "")}

    Compare the resume with the job description.

    Rules:
    - Match score must be between 0 and 100.
    - Consider skills, experience, education and keywords.
    - Only include skills actually found in the resume.
    - Missing skills should come from the job description only.
    - Keep every list short (maximum 5 items).
    - Suggestions should be practical and specific.
    - Return ONLY valid JSON.
    - No markdown.
    - No explanations.
    - No extra text.

    Return this format exactly:

    {{
        "match_score": 0,
        "matching_skills": [],
        "missing_skills": [],
        "strengths": [],
        "suggestions": []
    }}
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini returns it
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)

    except Exception as e:
        print("AI MATCH ERROR:", e)
        raise