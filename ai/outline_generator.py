import openai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (useful for keeping API keys secure)
load_dotenv()

# Set the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_outline(title, learning_outcomes):
    """
    Generates a high-level course outline using OpenAI GPT-4o,
    based on the course title and learning outcomes.
    """

    # Construct the prompt for the AI model
    prompt = f"""
    You are an expert course designer. Based on the following course title and learning outcomes,
    generate a high-level outline of suggested topics/modules.

    Title: {title}

    Learning Outcomes:
    {', '.join(learning_outcomes)}

    Suggested Course Outline:
    """

    # Call OpenAI's ChatCompletion endpoint with the constructed prompt
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Use the GPT-4o model
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # Controls creativity/randomness (0 = deterministic, 1 = creative)
        max_tokens=500    # Limit output length
    )

    # Extract and return the AI-generated content (course outline), removing leading/trailing whitespace
    return response['choices'][0]['message']['content'].strip()
