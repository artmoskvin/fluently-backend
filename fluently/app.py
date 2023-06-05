import os

import openai
from dotenv import load_dotenv
from flask import abort, Flask, request, jsonify

from fluently.completion import get_completion

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)


@app.route('/complete', methods=['POST'])
def complete():
    app.logger.info("Got request from the client!")

    text = request.json.get("text", None)

    if text:
        app.logger.info("Text: " + text)
        try:
            completion = get_completion(text)

            app.logger.info("Completion: " + completion)

            return jsonify({"completion": completion})
        except Exception as e:
            app.logger.error(f"Cannot create completion: {e}", exc_info=True)
            abort(500, description="Completion failed")

    abort(400, description="Text is empty")
