import requests
from conf import environment as env

class ApiClient:
    def __init__(self, token=None):
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def login(self, email, password):
        url = f"{env.API_URL}/login"
        payload = {"email": email, "password": password}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_user_info(self):
        url = f"{env.API_URL}/user"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
