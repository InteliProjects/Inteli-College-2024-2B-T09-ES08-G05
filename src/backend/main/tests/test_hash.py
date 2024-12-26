import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.modules.document.document_service import DocumentService
from app.modules.document.document_model import File

file = 'https://ecto-one-bucket.s3.us-east-1.amazonaws.com/a-decidir.png'
hash = '522785c0ab56e9e7de0cb3b8d26ad9f5dddb847c5a6193668fdfffca1a52e762'
checksum = '6024d52c'

@pytest.fixture
def mock_db_session():
    # Mock for the database session
    db = MagicMock()
    return db


@pytest.fixture
def mock_file():
    # Mock of a file for testing
    return File(file_id=1, url=file, hash=None, checksum=None)


def test_hash_file_success(mock_db_session, mock_file, mocker):
    # Mocking database query behavior
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_file

    # Creating an instance of DocumentService
    service = DocumentService(mock_db_session)

    # Calls the hash_file method
    result = service.hash_file(file_id=1)

    # Verifies if the hash was updated correctly
    assert result.hash == hash
    mock_db_session.commit.assert_called_once()  # Checks if commit was called


def test_hash_file_not_found(mock_db_session, mock_file, mocker):
    # Mock database query returning None (file not found)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    # Creating an instance of DocumentService
    service = DocumentService(mock_db_session)

    # Failure test: should raise HTTPException when file is not found
    with pytest.raises(HTTPException) as exc_info:
        service.hash_file(file_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "File not found."


def test_checksum_file_success(mock_db_session, mock_file, mocker):
    # Mock database query returning a valid file
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_file

    # Creating an instance of DocumentService
    service = DocumentService(mock_db_session)

    # Calls the checksum_file method
    result = service.checksum_file(file_id=1)

    # Verifies if the checksum was updated correctly
    assert result.checksum == checksum
    mock_db_session.commit.assert_called_once()  # Checks if commit was called


def test_checksum_file_not_found(mock_db_session, mock_file, mocker):
    # Mock database query returning None (file not found)
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    # Creating an instance of DocumentService
    service = DocumentService(mock_db_session)

    # Failure test: should raise HTTPException when file is not found
    with pytest.raises(HTTPException) as exc_info:
        service.checksum_file(file_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "File not found."
