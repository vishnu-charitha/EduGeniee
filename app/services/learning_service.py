from app.ai.gemini_client import generate_response
from app.ai.prompt_templates import learning_path_prompt


def generate_learning_path(topic: str):

    prompt = learning_path_prompt(topic)

    return generate_response(prompt)