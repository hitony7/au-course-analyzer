import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env (for secure API key access)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_outline(course_data):
    """
    Generates a high-level AI-recommended course outline based on full course data.
    Accepts a dictionary containing course details such as title, learning outcomes, topics, and overview.
    """

    # Extract key fields from the course JSON (use default fallbacks if missing)
    title = course_data.get("title") or course_data.get(
        "course_title", "Unknown Course"
    )
    learning_outcomes = course_data.get("learning_outcomes", [])
    overview = course_data.get("overview", "")
    outline = course_data.get("outline", [])
    evaluation = course_data.get("evaluation", [])

    # Construct a prompt using course metadata to guide the AI in generating a relevant outline
    prompt = f"""
You are an expert course designer. Based on the following real course data,
generate a high-level outline of suggested modules/units.

Course Title: {title}

Course Overview:
{overview}

Learning Outcomes:
{', '.join(learning_outcomes)}

Outline:
{', '.join(outline)}

Suggested Course Outline:
"""

    # Make a call to OpenAI's ChatCompletion API (GPT-4o model)
    response = openai.chat.completions.create(
        model="gpt-4o",  # Optimized version of GPT-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,  # Moderate creativity
        max_tokens=500,  # Limit output size
    )

    # Extract and return the text of the generated outline
    return response.choices[0].message.content.strip()
