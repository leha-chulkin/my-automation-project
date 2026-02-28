"""
Тестовые данные для проекта тестирования Авиасейлс.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from faker import Faker


@dataclass
class UserData:
    """Данные тестового пользователя."""
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str


@dataclass
class EventData:
    """Данные личного события."""
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str
    reminder_minutes: int = 30
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None


class TestDataGenerator:
    """Генератор тестовых данных."""
    
    def __init__(self, locale: str = "ru_RU"):
        self.faker = Faker(locale)
    
    def generate_user(self, email: Optional[str] = None, password: Optional[str] = None) -> UserData:
        """Генерирует данные тестового пользователя."""
        return UserData(
            email=email or self.faker.email(),
            password=password or self.faker.password(length=12, special_chars=True),
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            phone=self.faker.phone_number()
        )
    
    def generate_event(
        self,
        title: Optional[str] = None,
        days_from_now: int = 7
    ) -> EventData:
        """Генерирует данные личного события."""
        start_date = datetime.now() + timedelta(days=days_from_now)
        end_date = start_date + timedelta(hours=2)
        
        return EventData(
            title=title or f"Событие {self.faker.word()}",
            description=self.faker.text(max_nb_chars=200),
            start_date=start_date,
            end_date=end_date,
            location=self.faker.city(),
            reminder_minutes=self.faker.random_element([15, 30, 60, 120]),
            is_recurring=self.faker.boolean(chance_of_getting_true=30),
            recurrence_pattern="WEEKLY" if self.faker.boolean(chance_of_getting_true=30) else None
        )
    
    def generate_multiple_events(self, count: int = 5) -> List[EventData]:
        """Генерирует несколько личных событий."""
        return [self.generate_event(days_from_now=i) for i in range(1, count + 1)]


# Предопределенные тестовые данные
class TestData:
    """Предопределенные тестовые данные."""
    
    # Пользователи
    VALID_USER = UserData(
        email="test_aviasales@temp-mail.org",
        password="SecurePass123!",
        first_name="Иван",
        last_name="Тестов",
        phone="+79991234567"
    )
    
    INVALID_USER = UserData(
        email="invalid@example.com",
        password="wrongpassword",
        first_name="Неверный",
        last_name="Пользователь",
        phone="+79998887766"
    )
    
    # События
    SIMPLE_EVENT = EventData(
        title="Тестовое событие",
        description="Описание тестового события для проверки функционала",
        start_date=datetime.now() + timedelta(days=3),
        end_date=datetime.now() + timedelta(days=3, hours=2),
        location="Москва",
        reminder_minutes=30,
        is_recurring=False
    )
    
    RECURRING_EVENT = EventData(
        title="Еженедельная встреча",
        description="Еженедельная планерка команды",
        start_date=datetime.now() + timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1, hours=1),
        location="Онлайн",
        reminder_minutes=15,
        is_recurring=True,
        recurrence_pattern="WEEKLY"
    )
    
    URGENT_EVENT = EventData(
        title="Срочная задача",
        description="Выполнить срочную задачу",
        start_date=datetime.now() + timedelta(hours=1),
        end_date=datetime.now() + timedelta(hours=2),
        location="Офис",
        reminder_minutes=5,
        is_recurring=False
    )
    
    # Граничные значения
    LONG_TITLE = "A" * 100  # Максимальная длина заголовка
    LONG_DESCRIPTION = "B" * 500  # Максимальная длина описания
    EMPTY_TITLE = ""
    EMPTY_DESCRIPTION = ""
    
    # Специальные символы
    SPECIAL_CHARS_TITLE = "Событие !@#$%^&*()_+"
    SPECIAL_CHARS_DESCRIPTION = "Описание с <>[]{}|\\/~`"


# Создаем экземпляры генераторов
data_generator = TestDataGenerator()
