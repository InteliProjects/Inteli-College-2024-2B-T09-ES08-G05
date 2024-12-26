import pytest
import re
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.modules.user.user_service import UserService
from app.modules.user.user_schemas import LoginRequest
from app.modules.user.user_model import User

# Mock for the UserService class
@pytest.fixture
def mock_db():
    mock = MagicMock()
    return mock

@pytest.fixture
def user_service(mock_db):
    return UserService(mock_db)

# Utility function to get the last log entry from the log file
def get_last_log(log_filename="logs/user.log"):
    with open(log_filename, "r") as log_file:
        lines = log_file.readlines()
    return lines[-1] if lines else None

# Test for successful login
def test_login_successful(user_service):
    login_data = LoginRequest(email="joselitojuniormc@gmail.com", password="joselito123")
    
    # Simulate the database response (valid user found)
    user_service.db.query().filter().first.return_value = User(id=1, email="joselitojuniormc@gmail.com", password="joselito123")
    
    # Call the login function, which will use the mocked database
    user = user_service.login(email=login_data.email, password=login_data.password)

    # Verify the returned data
    assert user.email == "joselitojuniormc@gmail.com"
    assert user.password == "joselito123"
    assert user.id == 1

    # Verify the last log entry
    last_log = get_last_log("logs/user.log")
    print(last_log)

    expected_log_pattern = r"User ID: 1 - Action: LOGIN - User logged in successfully."
    assert re.search(expected_log_pattern, last_log) is not None

# Test for login failure
def test_login_failure(user_service):
    login_data = LoginRequest(email="notfound@example.com", password="wrongpassword")
    
    # Simulate the database response (no user found)
    user_service.db.query().filter().first.return_value = None
    
    # Call the login function, which will use the mocked database
    with pytest.raises(HTTPException) as exc_info:
        user_service.login(email=login_data.email, password=login_data.password)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"

    # Verify the last log entry
    last_log = get_last_log("logs/user.log")
    assert last_log is not None
    
    # Regex to check if the log matches the expected structure
    expected_log_pattern = r"User email: notfound@example.com - Action: LOGIN_FAILED - Invalid email or password"
    assert re.search(expected_log_pattern, last_log) is not None
