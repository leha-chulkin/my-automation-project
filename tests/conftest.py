# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from api.client import APIClient
from config.settings import BASE_URL

@pytest.fixture(scope="session")
def driver() -> webdriver.Chrome:
    """Создаёт ChromeDriver для UI‑тестов."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # можно убрать, если нужен UI
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def login_page(driver) -> LoginPage:
    """Фикстура для LoginPage."""
    page = LoginPage(driver)
    page.open()
    return page

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Фикстура для API‑клиента."""
    return APIClient()
