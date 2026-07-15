from app.ai.gemini_client import generate_response
from app.ai.prompt_templates import qa_prompt


def ask_question(question: str):

    prompt = qa_prompt(question)

    return generate_response(prompt)