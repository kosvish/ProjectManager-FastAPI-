import smtplib
from email.message import EmailMessage
from celery import Celery
from src.config import SMTP_PASSWORD, SMTP_USER


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379")

# def get_email