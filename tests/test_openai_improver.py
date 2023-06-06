from unittest.mock import MagicMock

import pytest

from fluently.improvement.openai_improver import OpenAIImprover, OpenAIImproverException


def test_improve_success():
    text = "She don't sleep last night"
    expected_result = "She didn't sleep last night."

    mock_chat_llm = MagicMock()
    mock_chat_llm.return_value.content = expected_result

    improver = OpenAIImprover(mock_chat_llm)

    assert improver.improve(text) == expected_result
    mock_chat_llm.assert_called_once()


def test_improve_removes_quotes():
    text = "She don't sleep last night"
    expected_result = "She didn't sleep last night."

    mock_chat_llm = MagicMock()
    mock_chat_llm.return_value.content = f"\"{expected_result}\""

    improver = OpenAIImprover(mock_chat_llm)

    assert improver.improve(text) == expected_result
    mock_chat_llm.assert_called_once()


def test_improve_failure():
    text = "She don't sleep last night"

    mock_chat_llm = MagicMock()
    mock_chat_llm.side_effect = Exception("Improvement failed")

    improver = OpenAIImprover(mock_chat_llm)

    with pytest.raises(OpenAIImproverException) as e_info:
        improver.improve(text)

    assert str(e_info.value) == "OpenAI improvement failed"
    mock_chat_llm.assert_called_once()
