from unittest.mock import patch, create_autospec

from flask import current_app

from fluently import OpenAITranslator, OpenAIImprover


@patch('fluently.text.get_completion', return_value=" Groot")
def test_complete_succeeds(mock_get_completion, client, app):
    response = client.post("/text/complete", json={
        "text": "I am"
    })
    assert response.status_code == 200
    assert response.json["completion"] == " Groot"
    mock_get_completion.assert_called_once_with("I am")


@patch('fluently.text.get_completion', side_effect=Exception("Test"))
def test_complete_fails(mock_get_completion, client):
    response = client.post("/text/complete", json={
        "text": "I am"
    })
    assert response.status_code == 500
    assert "Completion failed" in response.text
    mock_get_completion.assert_called_once_with("I am")


def test_complete_text_is_empty(client):
    response = client.post("/text/complete", json={})
    assert response.status_code == 400
    assert "Text is empty" in response.text


def test_translate_succeeds(app, client):
    mock_translator = create_autospec(OpenAITranslator)
    mock_translator.translate.return_value = "Hello!"

    with app.app_context():
        current_app.config["OPENAI_TRANSLATOR"] = mock_translator

    response = client.post("/text/translate", json={
        "text": "Привет!"
    })
    assert response.status_code == 200
    assert response.json["translation"] == "Hello!"
    mock_translator.translate.assert_called_once_with("Привет!")


def test_translate_fails(app, client):
    mock_translator = create_autospec(OpenAITranslator)
    mock_translator.translate.side_effect = Exception("Test")

    with app.app_context():
        current_app.config["OPENAI_TRANSLATOR"] = mock_translator

    response = client.post("/text/translate", json={
        "text": "Привет!"
    })
    assert response.status_code == 500
    assert "Translation failed" in response.text
    mock_translator.translate.assert_called_once_with("Привет!")


def test_translate_text_is_empty(client):
    response = client.post("/text/translate", json={})
    assert response.status_code == 400
    assert "Text is empty" in response.text


def test_improve_succeeds(app, client):
    mock_improver = create_autospec(OpenAIImprover)
    mock_improver.improve.return_value = "She didn't sleep last night."

    with app.app_context():
        current_app.config["OPENAI_IMPROVER"] = mock_improver

    response = client.post("/text/improve", json={
        "text": "She don't sleep last night"
    })
    assert response.status_code == 200
    assert response.json["improvement"] == "She didn't sleep last night."
    mock_improver.improve.assert_called_once_with("She don't sleep last night")


def test_improve_fails(app, client):
    mock_improver = create_autospec(OpenAIImprover)
    mock_improver.improve.side_effect = Exception("Test")

    with app.app_context():
        current_app.config["OPENAI_IMPROVER"] = mock_improver

    response = client.post("/text/improve", json={
        "text": "She don't sleep last night"
    })
    assert response.status_code == 500
    assert "Improvement failed" in response.text
    mock_improver.improve.assert_called_once_with("She don't sleep last night")


def test_improve_text_is_empty(client):
    response = client.post("/text/improve", json={})
    assert response.status_code == 400
    assert "Text is empty" in response.text
