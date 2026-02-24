# tests/test_ui.py
import allure
import pytest
from config.secrets import LOGIN_EMAIL, LOGIN_PASSWORD

@allure.feature("UI")
@allure.story("Вход в систему")
@allure.title("Проверка успешного входа")
@pytest.mark.ui
def test_login_success(login_page):
    login_page.enter_email(LOGIN_EMAIL)
    login_page.enter_password(LOGIN_PASSWORD)
    login_page.submit()
    login_page.assert_success()
