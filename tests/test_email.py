import pytest
from app.emailer import send_email

def test_send_email(mocker):
    #Verifica que la función envía un correo correctamente.
    mock_smtp = mocker.patch('smtplib.SMTP')
    
    send_email("user@gmail.com", "Archivo cambiado a privado")
    
    mock_smtp.assert_called_once()
