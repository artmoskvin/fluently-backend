import pytest
from unittest.mock import MagicMock
from fluently.translation.openai_translator import OpenAITranslator, OpenAITranslatorException


def test_translate_success():
    text = "Привет! Как дела?"
    expected_result = "Hello! How are you?"

    mock_chat_llm = MagicMock()
    mock_chat_llm.return_value.content = expected_result

    translator = OpenAITranslator(mock_chat_llm)

    assert translator.translate(text) == expected_result
    mock_chat_llm.assert_called_once()


def test_translate_failure():
    text = "Привет! Как дела?"

    mock_chat_llm = MagicMock()
    mock_chat_llm.side_effect = Exception("Translation failed")

    translator = OpenAITranslator(mock_chat_llm)

    with pytest.raises(OpenAITranslatorException) as e_info:
        translator.translate(text)

    assert str(e_info.value) == "OpenAI translation failed"
    mock_chat_llm.assert_called_once()
