import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_outline(title, learning_outcomes):
    prompt = f"""
    You are an expert course designer. Based on the following course title and learning outcomes,
    generate a high-level outline of suggested topics/modules.

    Title: {title}

    Learning Outcomes:
    {', '.join(learning_outcomes)}

    Suggested Course Outline:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()