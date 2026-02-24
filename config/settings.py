# config/settings.py
import os

BASE_URL: str = os.getenv("BASE_URL", "https://example.com")
API_BASE_URL: str = os.getenv("API_BASE_URL", f"{BASE_URL}/api")
TIMEOUT: int = int(os.getenv("TIMEOUT", "10"))
