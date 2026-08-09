import os

from dotenv import load_dotenv
from google import genai

from utils.rag import retrieve_context
from utils.memory import get_messages


load_dotenv()


# ------------------ Gemini Client ------------------

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# ------------------ AI Assistant ------------------

def ask_ai(prompt, resume_text=""):

    try:

        # ------------------ Conversation Memory ------------------

        messages = get_messages()

        conversation = ""

        # Last few messages only
        for message in messages[-10:]:

            role = message.get("role", "user")
            content = message.get("content", "")

            conversation += (
                f"{role.upper()}: {content}\n"
            )


        # ------------------ Resume Context ------------------

        context = ""

        if resume_text:

            try:

                context = retrieve_context(prompt)

            except Exception:

                context = resume_text[:6000]


        # ------------------ Full AI Prompt ------------------

        full_prompt = f"""
You are JobConnect AI, a friendly and intelligent AI Career Assistant.

You can have normal conversations with the user.
You are NOT only a job-search assistant.

Your responsibilities:

1. Have normal conversations naturally.
2. Answer general questions clearly.
3. Help with career guidance.
4. Analyze the user's resume when relevant.
5. Suggest skills and learning roadmaps.
6. Help with interview preparation.
7. Help improve resumes.
8. Give personalized career advice when resume information is available.
9. Remember and use relevant previous conversation context.
10. Do NOT pretend every question is a job-search request.

IMPORTANT:
- If the user says hello, hi, thanks, how are you, etc., respond naturally.
- If the user asks a general knowledge question, answer normally.
- If the user asks a career question, provide useful career guidance.
- If the user asks about their resume, use the resume information.
- If the user asks about previous conversation, use the conversation history.
- Do not force career advice into unrelated casual conversations.
- Be friendly, concise and helpful.
- Do not say that you are unable to answer just because a question is not about jobs.

------------------ Previous Conversation ------------------

{conversation}

------------------ Resume Context ------------------

{context}

------------------ Current User Message ------------------

{prompt}

------------------ Response ------------------

Answer the user's current message naturally and directly.
"""


        # ------------------ Gemini ------------------

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )


        return response.text


    except Exception as e:

        return (
            "⚠️ AI service is temporarily unavailable.\n\n"
            f"{str(e)}"
        )