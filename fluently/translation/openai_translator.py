import logging

from langchain import PromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.schema import SystemMessage, HumanMessage

from fluently.translation.translator import Translator

TRANSLATION_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="Translate into English: {text}",
)

logger = logging.getLogger(__name__)


class OpenAITranslator(Translator):

    def __init__(self, chat_llm: BaseChatModel):
        self.chat_llm = chat_llm

    def translate(self, text: str) -> str:
        messages = [SystemMessage(content="You are a helpful assistant."),
                    HumanMessage(content=TRANSLATION_PROMPT.format(text=text))]

        try:
            return self.chat_llm(messages).content
        except Exception as e:
            logger.error("OpenAI translation failed", exc_info=e)
            raise OpenAITranslatorException("OpenAI translation failed") from e


class OpenAITranslatorException(Exception):
    pass
