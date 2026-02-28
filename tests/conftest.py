"""
Конфигурационные фикстуры для тестов.
"""
import pytest
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.settings import settings
from config.test_data import TestData, TestDataGenerator
from pages.login_page import LoginPage
from pages.personal_events_page import PersonalEventsPage
from api.auth_api import AuthAPI
from api.events_api import EventsAPI


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Добавление кастомных опций командной строки."""
    parser.addoption(
        "--browser",
        action="store",
        default=settings.browser,
        help="Браузер для тестов: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=settings.headless,
        help="Запуск в headless режиме"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=settings.aviasales_url,
        help="Базовый URL для тестов"
    )


@pytest.fixture(scope="session")
def test_data():
    """Фикстура с тестовыми данными."""
    return TestData()


@pytest.fixture(scope="session")
def data_generator():
    """Фикстура с генератором тестовых данных."""
    return TestDataGenerator()


@pytest.fixture(scope="session")
def auth_api():
    """Фикстура с API клиентом авторизации."""
    return AuthAPI()


@pytest.fixture
def events_api(auth_token):
    """Фикстура с API клиентом событий."""
    return EventsAPI(auth_token)


@pytest.fixture(scope="session")
def browser_type(request):
    """Определение типа браузера из командной строки."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Определение headless режима из командной строки."""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def base_url(request):
    """Определение базового URL из командной строки."""
    return request.config.getoption("--base-url")


@pytest.fixture
def driver(browser_type, headless_mode):
    """
    Фикстура для создания WebDriver.
    
    Args:
        browser_type: Тип браузера
        headless_mode: Режим без графического интерфейса
        
    Yields:
        WebDriver экземпляр
    """
    driver = None
    
    try:
        if browser_type.lower() == "chrome":
            options = ChromeOptions()
            if headless_mode:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-notifications")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser_type.lower() == "firefox":
            options = FirefoxOptions()
            if headless_mode:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            service = webdriver.firefox.service.Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
        elif browser_type.lower() == "edge":
            options = EdgeOptions()
            if headless_mode:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            
            service = webdriver.edge.service.Service(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_type}")
        
        # Настройка таймаутов
        driver.implicitly_wait(settings.implicit_wait)
        driver.set_page_load_timeout(settings.page_load_timeout)
        
        logger.info(f"Браузер {browser_type} запущен (headless: {headless_mode})")
        
        yield driver
        
    except Exception as e:
        logger.error(f"Ошибка при создании WebDriver: {str(e)}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("Браузер закрыт")


@pytest.fixture
def login_page(driver, base_url):
    """
    Фикстура для страницы авторизации.
    
    Args:
        driver: WebDriver экземпляр
        base_url: Базовый URL
        
    Returns:
        LoginPage экземпляр
    """
    page = LoginPage(driver)
    page.base_url = base_url
    return page


@pytest.fixture
def events_page(driver, base_url):
    """
    Фикстура для страницы личных событий.
    
    Args:
        driver: WebDriver экземпляр
        base_url: Базовый URL
        
    Returns:
        PersonalEventsPage экземпляр
    """
    page = PersonalEventsPage(driver)
    page.base_url = base_url
    return page


@pytest.fixture
def auth_token(auth_api, test_data):
    """
    Фикстура для получения токена авторизации.
    
    Args:
        auth_api: API клиент авторизации
        test_data: Тестовые данные
        
    Returns:
        Токен авторизации или None
    """
    response = auth_api.login_with_user_data(test_data.VALID_USER)
    if response.success:
        logger.info("Токен авторизации получен успешно")
        return response.token
    else:
        logger.warning(f"Не удалось получить токен: {response.error}")
        return None


@pytest.fixture
def authenticated_driver(driver, auth_token, base_url):
    """
    Фикстура для аутентифицированного драйвера.
    
    Args:
        driver: WebDriver экземпляр
        auth_token: Токен авторизации
        base_url: Базовый URL
        
    Returns:
        Аутентифицированный WebDriver
    """
    if auth_token:
        # Устанавливаем куки авторизации
        driver.get(base_url)
        driver.add_cookie({
            'name': 'auth_token',
            'value': auth_token,
            'domain': '.aviasales.ru',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })
        logger.info("Куки авторизации установлены")
    
    return driver


@pytest.fixture
def authenticated_events_page(authenticated_driver, base_url):
    """
    Фикстура для аутентифицированной страницы событий.
    
    Args:
        authenticated_driver: Аутентифицированный WebDriver
        base_url: Базовый URL
        
    Returns:
        PersonalEventsPage экземпляр
    """
    page = PersonalEventsPage(authenticated_driver)
    page.base_url = base_url
    return page


@pytest.fixture
def cleanup_events(events_api):
    """
    Фикстура для очистки событий после теста.
    
    Args:
        events_api: API клиент событий
        
    Yields:
        None
    """
    # Получаем список событий перед тестом
    response = events_api.get_events()
    event_ids = []
    
    if response.success:
        for event in response.events:
            event_ids.append(event.get('id'))
    
    yield
    
    # Удаляем все события после теста
    for event_id in event_ids:
        events_api.delete_event(event_id)
    
    logger.info(f"Очищено {len(event_ids)} событий")


@pytest.fixture
def create_test_event(events_api, data_generator):
    """
    Фикстура для создания тестового события.
    
    Args:
        events_api: API клиент событий
        data_generator: Генератор тестовых данных
        
    Returns:
        Функция для создания события
    """
    def _create_event(event_data=None):
        if event_data is None:
            event_data = data_generator.generate_event()
        
        response = events_api.create_event(event_data)
        if response.success:
            logger.info(f"Тестовое событие создано: {event_data.title}")
            return response.event_id, event_data
        else:
            logger.error(f"Не удалось создать тестовое событие: {response.error}")
            return None, None
    
    return _create_event


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания отчетов Allure.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Делаем скриншот при падении теста
        try:
            if "driver" in item.fixturenames:
                driver = item.funcargs["driver"]
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info("Скриншот при падении теста сохранен")
        except Exception as e:
            logger.error(f"Не удалось сделать скриншот: {str(e)}")


@pytest.fixture(autouse=True)
def log_test_name(request):
    """
    Автоматическая фикстура для логирования имени теста.
    """
    logger.info(f"Запуск теста: {request.node.name}")
    yield
    logger.info(f"Завершение теста: {request.node.name}")
