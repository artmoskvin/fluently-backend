import logging

from flask import Blueprint, request, jsonify, abort, current_app

from fluently import get_completion

logger = logging.getLogger(__name__)

bp = Blueprint('text', __name__, url_prefix='/text')


@bp.route('/complete', methods=['POST'])
def complete():
    logger.info("Received completion request")

    text = request.json.get("text", None)

    if text:
        logger.info("Text: " + text)
        try:
            completion = get_completion(text)

            logger.info("Completion: " + completion)

            return jsonify({"completion": completion})
        except Exception as e:
            logger.error(f"Completion failed: {e}", exc_info=True)
            abort(500, description="Completion failed")

    abort(400, description="Text is empty")


@bp.route("/translate", methods=["POST"])
def translate():
    logger.info("Received translation request")

    text = request.json.get("text", None)

    if text:
        logger.info("Text: " + text)
        try:
            translator = current_app.config['OPENAI_TRANSLATOR']
            translation = translator.translate(text)

            logger.info("Translation: " + translation)

            return jsonify({"translation": translation})
        except Exception as e:
            logger.error(f"Translation failed: {e}", exc_info=True)
            abort(500, description="Translation failed")

    abort(400, description="Text is empty")


@bp.route("/improve", methods=["POST"])
def improve():
    logger.info("Received improvement request")

    text = request.json.get("text", None)

    if text:
        logger.info("Text: " + text)
        try:
            improver = current_app.config['OPENAI_IMPROVER']
            improvement = improver.improve(text)

            logger.info("Improvement: " + improvement)

            return jsonify({"improvement": improvement})
        except Exception as e:
            logger.error(f"Improvement failed: {e}", exc_info=True)
            abort(500, description="Improvement failed")

    abort(400, description="Text is empty")
