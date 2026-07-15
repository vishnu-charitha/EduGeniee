from google import genai
from app.config import GEMINI_API_KEY
import time

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt):

    models = [
        "gemini-3.1-flash-lite",
        "gemini-3.1-flash",
        "gemini-2.5-flash-lite",
    ]

    last_error = None

    for model_name in models:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            return response.text

        except Exception as e:

            last_error = str(e)

            print(f"{model_name} failed: {last_error}")

            if "503" in last_error:
                time.sleep(2)
                continue

            if "429" in last_error:
                time.sleep(5)
                continue

            continue

    return (
        "🚧 EduGenie AI is currently experiencing high traffic.\n\n"
        "Please try again in a few moments.\n\n"
        f"Last Error: {last_error}"
    )