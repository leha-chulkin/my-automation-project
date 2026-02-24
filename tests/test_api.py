# tests/test_api.py
import allure
import pytest
from api.client import APIClient

@allure.feature("API")
@allure.story("Получение списка пользователей")
@allure.title("GET /users возвращает 200 и список")
@pytest.mark.api
def test_get_users(api_client: APIClient):
    response = api_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@allure.feature("API")
@allure.story("Создание нового пользователя")
@allure.title("POST /users создаёт пользователя и возвращает 201")
@pytest.mark.api
def test_create_user(api_client: APIClient):
    payload = {"name": "Test User", "email": "testuser@example.com"}
    response = api_client.post("/users", data=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
