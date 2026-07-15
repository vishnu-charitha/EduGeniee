from app.ai.gemini_client import generate_response
from app.ai.prompt_templates import explanation_prompt


def generate_explanation(topic: str):

    prompt = explanation_prompt(topic)

    return generate_response(prompt)