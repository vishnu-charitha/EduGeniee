from app.ai.gemini_client import generate_response
from app.ai.prompt_templates import qa_prompt


def generate_ai_response(question: str):

    prompt = qa_prompt(question)

    response = generate_response(prompt)

    return response