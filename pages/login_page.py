# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from allure import step

class LoginPage:
    """Page‑Object для страницы входа."""

    URL = f"{BASE_URL}/login"

    # locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @step("Открыть страницу входа")
    def open(self) -> None:
        self.driver.get(self.URL)

    @step("Ввести логин: {email}")
    def enter_email(self, email: str) -> None:
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    @step("Ввести пароль: {password}")
    def enter_password(self, password: str) -> None:
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    @step("Нажать кнопку входа")
    def submit(self) -> None:
        self.driver.find_element(*self.SUBMIT_BTN).click()

    @step("Проверить успешный вход")
    def assert_success(self) -> None:
        success = self.driver.find_element(*self.SUCCESS_MESSAGE)
        assert success.is_displayed(), "Успешное сообщение не найдено"
