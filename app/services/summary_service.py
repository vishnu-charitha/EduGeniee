from app.ai.gemini_client import generate_response
from app.ai.prompt_templates import summary_prompt


def generate_summary(text: str):

    prompt = summary_prompt(text)

    return generate_response(prompt)