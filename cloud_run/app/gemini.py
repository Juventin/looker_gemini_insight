import os
import re

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ.get('PROJECT_ID')


def remove_noise(text: str) -> str:
    text = re.sub("```html", "", text)
    text = re.sub("```", "", text)
    text = re.sub("##", "", text)

    # Converts text between double asterisks (**) to bold HTML tags.
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    return text.strip()


def split_sentences(text: str) -> list:
    """
    Splits a given text into individual sentences.
    This function uses a regular expression to split the text at periods, exclamation marks,
    and question marks, while ensuring that decimal numbers are not split.

    Args:
        text (str): The input text to be split into sentences.
    Returns:
        list: A list of sentences extracted from the input text, with leading and trailing
              whitespace removed from each sentence.
    """
    sentence_splitter = re.compile(r'(?<!\d)\.(?![\d,-])|(?<=[!?])')

    sentences = sentence_splitter.split(text)
    sentences = [sentence.strip()+'.'
                 for sentence in sentences if sentence.strip()]

    return sentences


def generate_summary(prompt: str) -> str:
    """
    Generate a summary of the given prompt using the Vertex AI Generative Model.

    Args:
        prompt (str): The prompt to generate a summary for.

    Returns:
        str: The generated summary. Limited to 5 sentences.
    """
    vertexai.init(project=PROJECT_ID, location="europe-west1")
    model = GenerativeModel(model_name="gemini-1.0-pro-002")

    response = model.generate_content(prompt)

    # Limit response to the first 5 sentences
    response = ' '.join(split_sentences(response.text)[:5])

    # Sometimes, Gemini writes bold as **text**, so we need to convert that to HTML
    result = remove_noise(response)
    return result
