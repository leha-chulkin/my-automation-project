# -*- coding: utf-8 -*-
import allure
from selenium.webdriver.common.by import By
from typing import Optional
from pages.base_page import BasePage
from config.test_data import UserData

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "input[name='remember']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Забыли пароль?")
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message, .alert-success")
    USER_MENU = (By.CSS_SELECTOR, ".user-menu, .profile-icon")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/login"
    
    @allure.step("Open login page")
    def open_login_page(self) -> None:
        """Open the login page."""
        self.open(self.url)
        self.wait_for_page_load()
    
    @allure.step("Enter email: {email}")
    def enter_email(self, email: str) -> None:
        """Type the email into the email input."""
        self.type_text(self.EMAIL_INPUT, email)
    
    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        """Type the password into the password input."""
        self.type_text(self.PASSWORD_INPUT, password)
    
    @allure.step("Click 'Login' button")
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str, remember_me: bool = False) -> None:
        """Perform login with provided credentials."""
        self.enter_email(email)
        self.enter_password(password)
        if remember_me:
            self.click(self.REMEMBER_ME_CHECKBOX)
        self.click_login_button()
        self.wait_for_page_load()
    
    @allure.step("Login using user data")
    def login_with_user_data(self, user_data: UserData, remember_me: bool = False) -> None:
        """Login with user data object."""
        self.login(user_data.email, user_data.password, remember_me)
    
    @allure.step("Check if error message is displayed")
    def is_error_displayed(self) -> bool:
        """Verify if an error message is visible."""
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)
    
    @allure.step("Get error message text")
    def get_error_message(self) -> Optional[str]:
        """Retrieve the error message text if it is visible."""
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    @allure.step("Check if login was successful")
    def is_login_successful(self) -> bool:
        """Verify successful login by checking presence of user menu or URL."""
        return (
            self.is_visible(self.USER_MENU, timeout=10) or
            "/dashboard" in self.get_current_url() or
            "/account" in self.get_current_url()
        )
    
    @allure.step("Click 'Forgot password?' link")
    def click_forgot_password(self) -> None:
        """Navigate to the forgot password page."""
        self.click(self.FORGOT_PASSWORD_LINK)
    
    @allure.step("Click 'Register' link")
    def click_register(self) -> None:
        """Navigate to the registration page."""
        self.click(self.REGISTER_LINK)
    
    @allure.step("Clear login form fields")
    def clear_login_fields(self) -> None:
        """Clear email and password input fields."""
        self.find_element(self.EMAIL_INPUT).clear()
        self.find_element(self.PASSWORD_INPUT).clear()
    
    @allure.step("Check if login form is displayed")
    def is_login_form_displayed(self) -> bool:
        """Verify the visibility of login form elements."""
        elements = [
            self.EMAIL_INPUT,
            self.PASSWORD_INPUT,
            self.LOGIN_BUTTON
        ]
        return all(self.is_visible(element, timeout=5) for element in elements)
    
    @allure.step("Set authentication cookie")
    def set_auth_cookie(self, auth_token: str) -> None:
        """Add authentication token as cookie."""
        self.driver.add_cookie({
            'name': 'auth_token',
            'value': auth_token,
            'domain': '.aviasales.ru',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })
        self.logger.info("Authentication cookie has been set")
    
    @allure.step("Get saved email from input")
    def get_saved_email(self) -> Optional[str]:
        """Retrieve the email value from the email input field."""
        element = self.find_element(self.EMAIL_INPUT)
        return element.get_attribute("value")
    
    @allure.step("Check if 'Remember me' checkbox is checked")
    def is_remember_me_checked(self) -> bool:
        """Determine if the 'Remember me' checkbox is selected."""
        element = self.find_element(self.REMEMBER_ME_CHECKBOX)
        return element.is_selected()
