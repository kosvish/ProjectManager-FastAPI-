import smtplib
from email.message import EmailMessage
from celery import Celery
from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379")


def get_email_template_dashboard(email: str, token: str):
    mail = EmailMessage()
    mail["Subject"] = "Confirm registration"
    mail["From"] = SMTP_USER
    mail["To"] = email

    mail.set_content(
        f"""
        <!DOCTYPE html>
<html lang="en">
<head>

</head>
<body>

  <div style="display: flex; align-items: center; justify-content: center;  flex-direction: column;">
    <h3>
      Account Verifaction
    </h3>
    <br>
    <p>
      Thanks for choosing our Service, please click on the button below to verify your account 
    </p>

    <a style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; 
    color: white;" href="http://localhost:8000/verification/?user_data={token}">
      Verify your email

    </a>
    <p>
      Please kindly ignore this email if you did not register nothing will happen. Thanks
    </p>

  </div>

</body>
</html>
        """,
        subtype='html'
    )

    return mail


@celery.task
def send_email_verification(email: str, token: str):
    mail = get_email_template_dashboard(email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(mail)
