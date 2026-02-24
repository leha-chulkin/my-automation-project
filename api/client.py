# api/client.py
import requests
from config.settings import API_BASE_URL
from config.secrets import API_TOKEN

class APIClient:
    """Простой клиент для взаимодействия с REST‑API."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    @property
    def base_url(self) -> str:
        return API_BASE_URL

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params, timeout=TIMEOUT)

    def post(self, endpoint: str, data: dict | None = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data, timeout=TIMEOUT)

    # Добавьте методы put, delete и т.д. по необходимости
