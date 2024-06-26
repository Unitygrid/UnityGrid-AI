import openai
import os

# commit removed

def generate_text(prompt):
    openai.api_key = os.getenv('OPENAI_API')
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()