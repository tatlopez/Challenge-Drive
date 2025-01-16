import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.drive import list_files, change_visibility, get_authenticated_user_email
from unittest.mock import patch, MagicMock


@patch('app.drive.get_drive_service')
def test_list_files(mock_get_service):
    #Testea que list_files() devuelve una lista de archivos simulada."""
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service

    mock_service.files().list().execute.return_value = {
        "files": [{"id": "123", "name": "test.txt", "mimeType": "text/plain"}]
    }

    files = list_files()
    
    assert len(files) == 1
    assert files[0]['id'] == "123"
    assert files[0]['name'] == "test.txt"


@patch('app.drive.get_drive_service')
def test_change_visibility(mock_get_service):
    #Testea que change_visibility() llama a la API correctamente.
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service

    file_id = "12345"
    change_visibility(file_id)

    mock_service.permissions().delete.assert_called_once_with(
        fileId=file_id, permissionId='anyoneWithLink'
    )


@patch('app.drive.get_drive_service')
def test_get_authenticated_user_email(mock_get_service):
    #Testea que se obtiene correctamente el email del usuario autenticado.
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service

    mock_service.about().get().execute.return_value = {
        "user": {"emailAddress": "testuser@example.com"}
    }

    email = get_authenticated_user_email()

    assert email == "testuser@example.com"
