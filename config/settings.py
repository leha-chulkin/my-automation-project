"""
Конфигурационные настройки проекта тестирования Авиасейлс.
Все чувствительные данные вынесены в переменные окружения.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки проекта."""
    
    # Базовые URL
    aviasales_url: str = Field(
        default="https://www.aviasales.ru",
        description="Базовый URL сайта Авиасейлс"
    )
    api_base_url: str = Field(
        default="https://api.aviasales.ru",
        description="Базовый URL API Авиасейлс"
    )
    
    # Тестовые данные
    test_email: str = Field(
        default="test_user@temp-mail.org",
        description="Email тестового пользователя"
    )
    test_password: str = Field(
        default="TestPassword123!",
        description="Пароль тестового пользователя"
    )
    
    # Настройки браузера
    browser: str = Field(default="chrome", description="Браузер для тестов")
    headless: bool = Field(default=False, description="Режим без графического интерфейса")
    implicit_wait: int = Field(default=10, description="Неявное ожидание в секундах")
    page_load_timeout: int = Field(default=30, description="Таймаут загрузки страницы")
    
    # Настройки API
    api_timeout: int = Field(default=10, description="Таймаут API запросов")
    api_retries: int = Field(default=3, description="Количество повторных попыток API")
    
    # Настройки тестов
    test_timeout: int = Field(default=60, description="Таймаут выполнения теста")
    rerun_failures: int = Field(default=2, description="Количество перезапусков упавших тестов")
    
    # Пути
    project_root: Path = Path(__file__).parent.parent
    test_data_dir: Path = project_root / "test_data"
    reports_dir: Path = project_root / "reports"
    screenshots_dir: Path = reports_dir / "screenshots"
    
    # Allure настройки
    allure_results_dir: Path = reports_dir / "allure-results"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Создаем экземпляр настроек
settings = Settings()

# Создаем необходимые директории
settings.reports_dir.mkdir(exist_ok=True)
settings.screenshots_dir.mkdir(exist_ok=True)
settings.allure_results_dir.mkdir(exist_ok=True)
settings.test_data_dir.mkdir(exist_ok=True)
