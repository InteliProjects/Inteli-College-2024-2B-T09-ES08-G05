from app.heartbeat import main
from unittest.mock import MagicMock
import os
import requests

USER_HOST = os.getenv('USER_HOST')

def test_heartbeat_successful(mocker):
    # Mock for requests.get
    mock_get = mocker.patch("app.heartbeat.requests.get")
    
    # Create a mocked response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed.total_seconds.return_value = 0.123
    mock_get.return_value = mock_response
    
    # Execute the main function
    latency, status = main()

    # Check result
    assert mock_get.return_value.status_code == 200
    assert latency == 123
    assert status is True

    # Verify if the API was called with the GET method and the correct route
    mock_get.assert_called_once_with(f"{USER_HOST}/users/heart")


def test_heartbeat_failure(mocker):
    # Mock for requests.get
    mock_get = mocker.patch("app.heartbeat.requests.get")
    
    # Create a mocked response for failure (404 error)
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    # Configure the mock to return the mocked response
    mock_get.return_value = mock_response
    
    # Execute the main function, which should handle the exception
    latency, status = main()

    # Check result
    assert latency is None
    assert status is False

    # Verify if the API was called with the GET method and the correct route
    mock_get.assert_called_once_with(f"{USER_HOST}/users/heart")
