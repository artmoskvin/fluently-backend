import os

import openai
from dotenv import load_dotenv
from flask import abort, Flask, request, jsonify
from langchain.chat_models import ChatOpenAI

from fluently.completion import get_completion
from fluently.improvement.openai_improver import OpenAIImprover
from fluently.translation.openai_translator import OpenAITranslator

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

chat_llm = ChatOpenAI()
translator = OpenAITranslator(chat_llm)
improver = OpenAIImprover(chat_llm)

app = Flask(__name__)


@app.route('/complete', methods=['POST'])
def complete():
    app.logger.info("Received completion request")

    text = request.json.get("text", None)

    if text:
        app.logger.info("Text: " + text)
        try:
            completion = get_completion(text)

            app.logger.info("Completion: " + completion)

            return jsonify({"completion": completion})
        except Exception as e:
            app.logger.error(f"Completion failed: {e}", exc_info=True)
            abort(500, description="Completion failed")

    abort(400, description="Text is empty")


@app.route("/translate", methods=["POST"])
def translate():
    app.logger.info("Received translation request")

    text = request.json.get("text", None)

    if text:
        app.logger.info("Text: " + text)
        try:
            translation = translator.translate(text)

            app.logger.info("Translation: " + translation)

            return jsonify({"translation": translation})
        except Exception as e:
            app.logger.error(f"Translation failed: {e}", exc_info=True)
            abort(500, description="Translation failed")

    abort(400, description="Text is empty")


@app.route("/improve", methods=["POST"])
def improve():
    app.logger.info("Received improvement request")

    text = request.json.get("text", None)

    if text:
        app.logger.info("Text: " + text)
        try:
            improvement = improver.improve(text)

            app.logger.info("Improvement: " + improvement)

            return jsonify({"improvement": improvement})
        except Exception as e:
            app.logger.error(f"Improvement failed: {e}", exc_info=True)
            abort(500, description="Improvement failed")

    abort(400, description="Text is empty")
