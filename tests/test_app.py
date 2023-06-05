from unittest.mock import patch

from fluently.app import app


@patch('fluently.app.get_completion', return_value=" Groot")
def test_complete_succeeds(mock_get_completion):
    with app.test_client() as client:
        response = client.post("/complete", json={
            "text": "I am"
        })
    assert response.status_code == 200
    assert response.json["completion"] == " Groot"
    mock_get_completion.assert_called_once_with("I am")


@patch('fluently.app.get_completion', side_effect=Exception("Test"))
def test_complete_fails(mock_get_completion):
    with app.test_client() as client:
        response = client.post("/complete", json={
            "text": "I am"
        })
    assert response.status_code == 500
    assert "Completion failed" in response.text
    mock_get_completion.assert_called_once_with("I am")


def test_text_is_empty():
    with app.test_client() as client:
        response = client.post("/complete", json={})
    assert response.status_code == 400
    assert "Text is empty" in response.text
