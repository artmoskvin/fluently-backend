import logging

from langchain import PromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.schema import SystemMessage, HumanMessage

from fluently.improvement.improver import Improver

IMPROVEMENT_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Improve writing for the text below. Don't provide any explanations. \
Don't wrap the improved text in quotes.

Text: {text}""",
)

logger = logging.getLogger(__name__)


class OpenAIImprover(Improver):
    def __init__(self, chat_llm: BaseChatModel):
        self.chat_llm = chat_llm

    def improve(self, text: str) -> str:
        messages = [SystemMessage(content="You are a helpful assistant."),
                    HumanMessage(content=IMPROVEMENT_PROMPT.format(text=text))]

        try:
            return self.chat_llm(messages).content.lstrip("\"").rstrip("\"")
        except Exception as e:
            logger.error("OpenAI improvement failed", exc_info=e)
            raise OpenAIImproverException("OpenAI improvement failed") from e


class OpenAIImproverException(Exception):
    pass
