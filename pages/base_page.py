"""
Базовый класс для всех Page Objects.
"""
import allure
import logging
from typing import Optional, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from config.settings import settings


class BasePage:
    """Базовый класс для всех страниц."""
    
    def __init__(self, driver: WebDriver, timeout: int = None):
        """
        Инициализация базовой страницы.
        
        Args:
            driver: WebDriver экземпляр
            timeout: Таймаут ожидания элементов
        """
        self.driver = driver
        self.timeout = timeout or settings.implicit_wait
        self.wait = WebDriverWait(driver, self.timeout)
        self.logger = logging.getLogger(__name__)
        self.base_url = settings.aviasales_url
    
    @allure.step("Открыть страницу {url}")
    def open(self, url: str = "") -> None:
        """
        Открыть указанный URL.
        
        Args:
            url: URL для открытия (относительный или абсолютный)
        """
        full_url = f"{self.base_url}/{url.lstrip('/')}" if url else self.base_url
        self.driver.get(full_url)
        self.logger.info(f"Открыта страница: {full_url}")
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "WebElement":
        """
        Найти элемент с ожиданием.
        
        Args:
            locator: Кортеж (By, значение)
            timeout: Время ожидания
            
        Returns:
            Найденный элемент
            
        Raises:
            TimeoutException: Если элемент не найден за указанное время
        """
        wait_timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"Элемент найден: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Элемент не найден: {locator}")
            raise
    
    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> list:
        """
        Найти все элементы с ожиданием.
        
        Args:
            locator: Кортеж (By, значение)
            timeout: Время ожидания
            
        Returns:
            Список найденных элементов
        """
        wait_timeout = timeout or self.timeout
        try:
            elements = WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            self.logger.debug(f"Найдено {len(elements)} элементов: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"Элементы не найдены: {locator}")
            return []
    
    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Кликнуть по элементу.
        
        Args:
            locator: Кортеж (By, значение)
            timeout: Время ожидания
        """
        element = self.find_element(locator, timeout)
        element.click()
        self.logger.debug(f"Клик по элементу: {locator}")
    
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def type_text(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> None:
        """
        Ввести текст в элемент.
        
        Args:
            locator: Кортеж (By, значение)
            text: Текст для ввода
            timeout: Время ожидания
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"Введен текст '{text}' в элемент: {locator}")
    
    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        Получить текст элемента.
        
        Args:
            locator: Кортеж (By, значение)
            timeout: Время ожидания
            
        Returns:
            Текст элемента
        """
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"Получен текст '{text}' из элемента: {locator}")
        return text
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Проверить видимость элемента.
        
        Args:
            locator: Кортеж (By, значение)
            timeout: Время ожидания
            
        Returns:
            True если элемент видим, иначе False
        """
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Элемент видим: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Элемент не видим: {locator}")
            return False
    
    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Сделать скриншот и сохранить в allure.
        
        Args:
            name: Имя скриншота
            
        Returns:
            Путь к сохраненному скриншоту
        """
        screenshot_path = settings.screenshots_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"Скриншот сохранен: {screenshot_path}")
        return str(screenshot_path)
    
    @allure.step("Навести курсор на элемент {locator}")
    def hover(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Навести курсор на элемент.
        
        Args:
            locator: Кортеж (By, значение)
            timeout: Время ожидания
        """
        element = self.find_element(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
        self.logger.debug(f"Наведен курсор на элемент: {locator}")
    
    @allure.step("Выполнить JavaScript: {script}")
    def execute_script(self, script: str, *args) -> any:
        """
        Выполнить JavaScript код.
        
        Args:
            script: JavaScript код
            *args: Аргументы для скрипта
            
        Returns:
            Результат выполнения скрипта
        """
        result = self.driver.execute_script(script, *args)
        self.logger.debug(f"Выполнен JavaScript: {script}")
        return result
    
    @allure.step("Дождаться загрузки страницы")
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Дождаться полной загрузки страницы.
        
        Args:
            timeout: Время ожидания
        """
        wait_timeout = timeout or settings.page_load_timeout
        WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("Страница полностью загружена")
    
    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """
        Получить текущий URL.
        
        Returns:
            Текущий URL
        """
        url = self.driver.current_url
        self.logger.debug(f"Текущий URL: {url}")
        return url
    
    @allure.step("Обновить страницу")
    def refresh_page(self) -> None:
        """Обновить текущую страницу."""
        self.driver.refresh()
        self.wait_for_page_load()
        self.logger.debug("Страница обновлена")
