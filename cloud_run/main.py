import os
from flask import Flask, send_file, abort, request
from flask_cors import CORS

from app.format_data import convert_looker_data_to_markdown
from app.gemini import generate_summary

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


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
    file_path = 'visualization/looker_gemini_insight.js'

    try:
        return send_file(file_path)

    # If the file is not found, raise a 404 error with a description
    except FileNotFoundError:
        abort(404, description="File not found")


@app.route('/fortune_teller.png')
def get_fortune_teller():
    """
    Endpoint to send the image 'fortune_teller.png' for visualization.

    Returns:
        The image 'fortune_teller.png' if found.
        If the file is not found, returns a 404 error with a description.
    """
    file_path = 'visualization/fortune_teller.png'

    try:
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
    data = request.json

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
    data = request.json

    # Construct the prompt by concatenating a fixed string with the Markdown data
    prompt = "Write a one-paragraph summary predicting the future using the following data : \n\n"
    markdown = convert_looker_data_to_markdown(data)

    # Generate a summary using the prompt
    r = generate_summary(prompt + markdown)

    return r


@app.route('/testmd', methods=['POST'])
def testmd():
    data = request.json

    prompt = "Write a one-paragraph summary interpreting the following data:\n\n"
    markdown = convert_looker_data_to_markdown(data)

    return prompt + markdown


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Developed by Jeremy Juventin
