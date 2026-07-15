import json

from app.ai.gemini_client import generate_response
from app.ai.prompt_templates import quiz_prompt


def generate_quiz(topic: str):

    prompt = quiz_prompt(topic)

    response = generate_response(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    return json.loads(response)