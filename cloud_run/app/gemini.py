import os
import re

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ.get('PROJECT_ID')


def remove_noise(text):
    text = re.sub("```html", "", text)
    text = re.sub("```", "", text)
    text = re.sub("##", "", text)

    # Converts text between double asterisks (**) to bold HTML tags.
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    return text.strip()

def generate_summary(prompt):
    """
    Generate a summary of the given prompt using the Vertex AI Generative Model.

    Args:
        prompt (str): The prompt to generate a summary for.

    Returns:
        str: The generated summary.
    """
    vertexai.init(project=PROJECT_ID, location="europe-west1")
    model = GenerativeModel(model_name="gemini-1.0-pro-002")

    response = model.generate_content(prompt)

    # Sometimes, Gemini writes bold as **text**, so we need to convert that to HTML
    result = remove_noise(response.text)
    return result

# Developed by Jeremy Juventin
