from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


DB_TEST_USER = os.getenv("DB_TEST_USER")
DB_TEST_PASSWORD = os.getenv("DB_TEST_PASSWORD")
DB_TEST_HOST = os.getenv("DB_TEST_HOST")
DB_TEST_PORT = os.getenv("DB_TEST_PORT")
DB_TEST_NAME = os.getenv("DB_TEST_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORYTHM = os.getenv("ALGORYTHM")

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_USER = os.getenv("SMTP_USER")
