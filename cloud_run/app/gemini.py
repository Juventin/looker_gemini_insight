import os
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ.get('PROJECT_ID')


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
    return response.text


# Developed by Jeremy Juventin
