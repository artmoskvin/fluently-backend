import os

import openai
from dotenv import load_dotenv
from flask import Flask
from langchain.chat_models import ChatOpenAI

from fluently.completion import get_completion
from fluently.improvement.openai_improver import OpenAIImprover
from fluently.translation.openai_translator import OpenAITranslator


def create_app(test_config=None):
    load_dotenv()

    openai.api_key = os.environ.get('OPENAI_API_KEY')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

        chat_llm = ChatOpenAI()

        app.config['OPENAI_TRANSLATOR'] = OpenAITranslator(chat_llm)
        app.config['OPENAI_IMPROVER'] = OpenAIImprover(chat_llm)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import text
    app.register_blueprint(text.bp)

    return app
