import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(to_address, file_name):
    sender_email = os.getenv('EMAIL_ADDRESS')
    sender_password = os.getenv('EMAIL_PASSWORD')

    message = MIMEText(f"La visibilidad del archivo '{file_name}' ha sido cambiada a privada.")
    message['Subject'] = 'Cambio de visibilidad en Google Drive'
    message['From'] = sender_email
    message['To'] = to_address

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_address, message.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
