import requests
from configs.env_config import API_BASE_URL, AUTH_TOKEN
from configs.test_data import VALID_EMAIL, VALID_PASSWORD

def test_get_events():
    url = f"{API_BASE_URL}/events"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_login_api():
    url = f"{API_BASE_URL}/login"
    payload = {"email": VALID_EMAIL, "password": VALID_PASSWORD}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    json_response = response.json()
    assert "token" in json_response

def test_create_event():
    url = f"{API_BASE_URL}/events"
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    payload = {"name": "Test Event"}
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Event"

def test_delete_event():

    event_id = 1
    url = f"{API_BASE_URL}/events/{event_id}"
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 204
