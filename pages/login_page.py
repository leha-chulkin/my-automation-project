"""
Page Object для страницы авторизации Авиасейлс.
"""
import allure
from selenium.webdriver.common.by import By
from typing import Optional
from pages.base_page import BasePage
from config.test_data import UserData

class LoginPage(BasePage):
    """Page Object для страницы авторизации."""
    
    # Локаторы
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
    
    @allure.step("Открыть страницу авторизации")
    def open_login_page(self) -> None:
        """Открыть страницу авторизации."""
        self.open(self.url)
        self.wait_for_page_load()
    
    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str) -> None:
        """
        Ввести email в поле ввода.
        
        Args:
            email: Email для ввода
        """
        self.type_text(self.EMAIL_INPUT, email)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> None:
        """
        Ввести пароль в поле ввода.
        
        Args:
            password: Пароль для ввода
        """
        self.type_text(self.PASSWORD_INPUT, password)
    
    @allure.step("Нажать кнопку 'Войти'")
    def click_login_button(self) -> None:
        """Нажать кнопку входа."""
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Выполнить авторизацию с email: {email}")
    def login(self, email: str, password: str, remember_me: bool = False) -> None:
        """
        Выполнить полную авторизацию.
        
        Args:
            email: Email пользователя
            password: Пароль пользователя
            remember_me: Запомнить пользователя
        """
        self.enter_email(email)
        self.enter_password(password)
        
        if remember_me:
            self.click(self.REMEMBER_ME_CHECKBOX)
        
        self.click_login_button()
        self.wait_for_page_load()
    
    @allure.step("Авторизация с данными пользователя")
    def login_with_user_data(self, user_data: UserData, remember_me: bool = False) -> None:
        """
        Авторизация с использованием объекта UserData.
        
        Args:
            user_data: Данные пользователя
            remember_me: Запомнить пользователя
        """
        self.login(user_data.email, user_data.password, remember_me)
    
    @allure.step("Проверить наличие ошибки авторизации")
    def is_error_displayed(self) -> bool:
        """
        Проверить отображение ошибки авторизации.
        
        Returns:
            True если ошибка отображается, иначе False
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)
    
    @allure.step("Получить текст ошибки авторизации")
    def get_error_message(self) -> Optional[str]:
        """
        Получить текст ошибки авторизации.
        
        Returns:
            Текст ошибки или None если ошибки нет
        """
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    @allure.step("Проверить успешную авторизацию")
    def is_login_successful(self) -> bool:
        """
        Проверить успешность авторизации.
        
        Returns:
            True если авторизация успешна, иначе False
        """
        # Проверяем наличие меню пользователя или редирект на главную
        return (
            self.is_visible(self.USER_MENU, timeout=10) or
            "/dashboard" in self.get_current_url() or
            "/account" in self.get_current_url()
        )
    
    @allure.step("Нажать 'Забыли пароль?'")
    def click_forgot_password(self) -> None:
        """Перейти на страницу восстановления пароля."""
        self.click(self.FORGOT_PASSWORD_LINK)
    
    @allure.step("Нажать 'Зарегистрироваться'")
    def click_register(self) -> None:
        """Перейти на страницу регистрации."""
        self.click(self.REGISTER_LINK)
    
    @allure.step("Очистить поля авторизации")
    def clear_login_fields(self) -> None:
        """Очистить поля email и пароля."""
        self.find_element(self.EMAIL_INPUT).clear()
        self.find_element(self.PASSWORD_INPUT).clear()
    
    @allure.step("Проверить отображение формы авторизации")
    def is_login_form_displayed(self) -> bool:
        """
        Проверить отображение всех элементов формы авторизации.
        
        Returns:
            True если все элементы отображаются, иначе False
        """
        elements = [
            self.EMAIL_INPUT,
            self.PASSWORD_INPUT,
            self.LOGIN_BUTTON
        ]
        
        return all(self.is_visible(element, timeout=5) for element in elements)
    
    @allure.step("Установить куки авторизации")
    def set_auth_cookie(self, auth_token: str) -> None:
        """
        Установить куки авторизации для bypass логина.
        
        Args:
            auth_token: Токен авторизации
        """
        self.driver.add_cookie({
            'name': 'auth_token',
            'value': auth_token,
            'domain': '.aviasales.ru',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })
        self.logger.info("Куки авторизации установлены")
    
    @allure.step("Получить сохраненный email")
    def get_saved_email(self) -> Optional[str]:
        """
        Получить сохраненный email из поля ввода.
        
        Returns:
            Сохраненный email или None
        """
        element = self.find_element(self.EMAIL_INPUT)
        return element.get_attribute("value")
    
    @allure.step("Проверить чекбокс 'Запомнить меня'")
    def is_remember_me_checked(self) -> bool:
        """
        Проверить состояние чекбокса 'Запомнить меня'.
        
        Returns:
            True если чекбокс отмечен, иначе False
        """
        element = self.find_element(self.REMEMBER_ME_CHECKBOX)
        return element.is_selected()
