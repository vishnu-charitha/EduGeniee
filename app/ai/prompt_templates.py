def qa_prompt(question: str):

    return f"""
You are EduGenie, an AI Educational Assistant.

Answer the following educational question accurately.

Question:
{question}

Provide a clear, beginner-friendly answer.
"""


def explanation_prompt(topic: str):

    return f"""
You are EduGenie, an AI educational tutor.

Explain the following topic in simple language.

Topic:
{topic}

Rules:

1. Explain step by step.
2. Use simple English.
3. Give one practical example.
4. Mention important points.
5. Keep it beginner friendly.
"""

def quiz_prompt(topic: str):

    return f"""
You are EduGenie.

Generate exactly 5 multiple-choice questions on the topic:

{topic}

Return ONLY valid JSON.

Format:

[
  {{
    "question":"...",
    "option_a":"...",
    "option_b":"...",
    "option_c":"...",
    "option_d":"...",
    "correct_answer":"A"
  }}
]

Do not include markdown.
Do not include explanations.
Return JSON only.
"""

def summary_prompt(text: str):

    return f"""
You are EduGenie.

Summarize the following educational content.

Rules:

1. Keep it concise.
2. Use bullet points.
3. Highlight important concepts.
4. Beginner friendly.

Content:

{text}
"""
def learning_path_prompt(topic: str):

    return f"""
You are EduGenie, an AI Educational Mentor.

Create a structured learning roadmap for:

Topic: {topic}

Include the following sections:

1. Beginner
2. Intermediate
3. Advanced
4. Recommended Resources

Keep it concise and beginner friendly.
Return plain text only.
"""