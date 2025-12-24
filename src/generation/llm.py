from google import genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(context: str, query: str) -> str:
    prompt = f"""
You are a Harry Potter book-accurate assistant.

Rules:
- Answer ONLY using the provided context.
- You MAY combine information from multiple context passages.
- Do NOT add facts not supported by the context.
- If the answer cannot be reasonably derived from the context, say:
  "The provided context does not explicitly state this."

Context:
{context}

Question:
{query}
"""



    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()

