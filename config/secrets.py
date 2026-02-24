# config/secrets.py
import os
from dotenv import load_dotenv

load_dotenv()  # загружает .env из корня проекта

LOGIN_EMAIL: str = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD: str = os.getenv("LOGIN_PASSWORD")
API_TOKEN: str = os.getenv("API_TOKEN")
