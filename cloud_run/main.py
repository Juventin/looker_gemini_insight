import os
from flask import Flask, send_file, abort, request

from app.format_data import convert_looker_data_to_markdown
from app.gemini import generate_summary

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/source')
def get_source():
    """
    Endpoint to send the JavaScript file 'looker_gemini_insight.js' for visualization.

    Returns:
        The JavaScript file 'looker_gemini_insight.js' if found.
        If the file is not found, returns a 404 error with a description.
    """
    # Define the path to the JavaScript file
    file_path = 'visualization/looker_gemini_insight.js'

    try:
        # Send the file as a response
        return send_file(file_path)

    # If the file is not found, raise a 404 error with a description
    except FileNotFoundError:
        abort(404, description="File not found")


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize the provided Looker data.

    Returns:
        The generated summary.
    """
    # Get the 'api_key' and 'looker_data' fields from the JSON payload
    gemini_key = request.json.get('api_key', '')
    data = request.json.get("looker_data")

    # Construct the prompt by concatenating a fixed string with the Markdown data
    prompt = "Write a one-paragraph summary interpreting the following data:\n\n"
    markdown = convert_looker_data_to_markdown(data)

    # Generate a summary using the prompt
    r = generate_summary(prompt + markdown)

    return r


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the future using the provided Looker data.

    Returns:
        The generated summary.
    """
    # Get the 'api_key' and 'looker_data' fields from the JSON payload
    gemini_key = request.json.get('api_key', '')
    data = request.json.get("looker_data")

    # Construct the prompt by concatenating a fixed string with the Markdown data
    prompt = "Write a one-paragraph summary predicting the future using the following data : \n\n"
    markdown = convert_looker_data_to_markdown(data)

    # Generate a summary using the prompt
    r = generate_summary(prompt + markdown)

    return r


@app.route('/testmd', methods=['POST'])
def testmd():
    # Endpoint to test the data without using Gemini credits
    gemini_key = request.json.get('api_key', '')
    data = request.json.get("looker_data")
    prompt = "Write a one-paragraph summary interpreting the following data:\n\n"
    markdown = convert_looker_data_to_markdown(data)

    return prompt + markdown


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
