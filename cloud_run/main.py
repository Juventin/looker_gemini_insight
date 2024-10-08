import os
from flask import Flask, send_file, abort, request, Response
from flask_cors import CORS

from app.format_data import convert_looker_data_to_markdown
from app.gemini import generate_summary

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SUMMARIZE_PROMPT = """
You are an experienced data analyst who has been summarizing complex data sets into concise and insightful reports for various stakeholders. Your expertise lies in extracting key insights and trends from raw data to aid decision-making processes.\n
Your task is to write a summary of 50 words interpreting the following data in an HTML paragraph, with bold tags on important elements if possible. Here is the data:\n\n
"""
PREDICT_PROMPT = """
You are an experienced data analyst with expertise in predicting future performances from diverse data sets. Your specialty lies in crafting insightful reports that highlight trends and future outcomes.\n
Your task is to write a summary of 50 words predicting the future performances using the following data in an HTML paragraph, with bold tags on important elements if possible. Here is the data:\n\n
"""

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/source.js')
def get_source():
    """
    Endpoint to send the JavaScript file 'looker_gemini_insight.js' for visualization.

    Returns:
        The JavaScript file 'looker_gemini_insight.js' if found.
        If the file is not found, returns a 404 error with a description.
    """
    file_path = 'visualization/looker_gemini_insight.js'
    cloud_run_url = request.url_root.replace('http://', 'https://')

    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(basedir, file_path)

        # Read file and replace <YOUR_CLOUD_RUN_URL> with request.url_root
        with open(filepath, 'r') as f:
            content = f.read()
            content = content.replace('<CLOUD_RUN_URL>', cloud_run_url)

            return Response(content, mimetype='text/javascript')


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
    try:
        data = request.json
        markdown = convert_looker_data_to_markdown(data)

        r = generate_summary(SUMMARIZE_PROMPT + markdown)
        return r

    except Exception as e:
        abort(400, description=e)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the future using the provided Looker data.

    Returns:
        The generated summary.
    """
    try:
        data = request.json
        markdown = convert_looker_data_to_markdown(data)

        r = generate_summary(PREDICT_PROMPT + markdown)
        return r

    except Exception as e:
        abort(400, description=e)

@app.route('/showprompt', methods=['POST'])
def showprompt():
    try:
        data = request.json
        markdown = convert_looker_data_to_markdown(data)

        result = SUMMARIZE_PROMPT + markdown

        # Replace all newlines with <br/> tags
        # result = result.replace('\n', '<br/>')

        return result

    except Exception as e:
        abort(400, description=e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
