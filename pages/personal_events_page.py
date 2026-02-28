"""
Page Object для страницы личных событий Авиасейлс.
"""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from typing import List, Optional, Tuple
from datetime import datetime

from pages.base_page import BasePage
from config.test_data import EventData


class PersonalEventsPage(BasePage):
    """Page Object для страницы личных событий."""
    
    # Основные локаторы
    EVENTS_SECTION = (By.CSS_SELECTOR, ".personal-events, .events-section")
    CREATE_EVENT_BUTTON = (By.CSS_SELECTOR, "button.create-event, a[href*='create-event']")
    EVENT_LIST = (By.CSS_SELECTOR, ".event-list .event-item, .events-grid .event-card")
    NO_EVENTS_MESSAGE = (By.CSS_SELECTOR, ".no-events, .empty-state")
    
    # Форма создания/редактирования события
    EVENT_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title'], #event-title")
    EVENT_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[name='description'], #event-description")
    EVENT_START_DATE_INPUT = (By.CSS_SELECTOR, "input[name='start_date'], #event-start")
    EVENT_END_DATE_INPUT = (By.CSS_SELECTOR, "input[name='end_date'], #event-end")
    EVENT_LOCATION_INPUT = (By.CSS_SELECTOR, "input[name='location'], #event-location")
    EVENT_REMINDER_SELECT = (By.CSS_SELECTOR, "select[name='reminder'], #event-reminder")
    EVENT_RECURRING_CHECKBOX = (By.CSS_SELECTOR, "input[name='is_recurring'], #event-recurring")
    EVENT_RECURRENCE_PATTERN_SELECT = (By.CSS_SELECTOR, "select[name='recurrence_pattern']")
    SAVE_EVENT_BUTTON = (By.CSS_SELECTOR, "button.save-event, button[type='submit']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "button.cancel-event, a.cancel")
    
    # Элементы события в списке
    EVENT_TITLE = (By.CSS_SELECTOR, ".event-title, .event-item h3")
    EVENT_DATE = (By.CSS_SELECTOR, ".event-date, .event-time")
    EVENT_LOCATION = (By.CSS_SELECTOR, ".event-location, .event-place")
    EVENT_ACTIONS = (By.CSS_SELECTOR, ".event-actions, .actions-menu")
    EDIT_EVENT_BUTTON = (By.CSS_SELECTOR, "button.edit-event, a.edit")
    DELETE_EVENT_BUTTON = (By.CSS_SELECTOR, "button.delete-event, a.delete")
    VIEW_EVENT_BUTTON = (By.CSS_SELECTOR, "button.view-event, a.view-details")
    
    # Фильтры и поиск
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-events, input[placeholder*='Поиск']")
    DATE_FILTER = (By.CSS_SELECTOR, "select.date-filter, input.filter-date")
    STATUS_FILTER = (By.CSS_SELECTOR, "select.status-filter")
    APPLY_FILTERS_BUTTON = (By.CSS_SELECTOR, "button.apply-filters")
    CLEAR_FILTERS_BUTTON = (By.CSS_SELECTOR, "button.clear-filters")
    
    # Модальные окна
    CONFIRM_DELETE_MODAL = (By.CSS_SELECTOR, ".confirm-delete-modal, .modal-delete")
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, "button.confirm-delete, .modal-confirm")
    CANCEL_DELETE_BUTTON = (By.CSS_SELECTOR, "button.cancel-delete, .modal-cancel")
    
    # Уведомления
    SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, ".alert-success, .notification-success")
    ERROR_NOTIFICATION = (By.CSS_SELECTOR, ".alert-error, .notification-error")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/personal/events"
    
    @allure.step("Открыть страницу личных событий")
    def open_events_page(self) -> None:
        """Открыть страницу личных событий."""
        self.open(self.url)
        self.wait_for_page_load()
    
    @allure.step("Проверить отображение раздела событий")
    def is_events_section_displayed(self) -> bool:
        """
        Проверить отображение раздела личных событий.
        
        Returns:
            True если раздел отображается, иначе False
        """
        return self.is_visible(self.EVENTS_SECTION, timeout=10)
    
    @allure.step("Нажать кнопку 'Создать событие'")
    def click_create_event(self) -> None:
        """Открыть форму создания события."""
        self.click(self.CREATE_EVENT_BUTTON)
    
    @allure.step("Заполнить форму события")
    def fill_event_form(self, event_data: EventData) -> None:
        """
        Заполнить форму события данными.
        
        Args:
            event_data: Данные события
        """
        self.type_text(self.EVENT_TITLE_INPUT, event_data.title)
        self.type_text(self.EVENT_DESCRIPTION_INPUT, event_data.description)
        
        # Форматирование дат для input[type="datetime-local"]
        start_date_str = event_data.start_date.strftime("%Y-%m-%dT%H:%M")
        end_date_str = event_data.end_date.strftime("%Y-%m-%dT%H:%M")
        
        self.type_text(self.EVENT_START_DATE_INPUT, start_date_str)
        self.type_text(self.EVENT_END_DATE_INPUT, end_date_str)
        
        if event_data.location:
            self.type_text(self.EVENT_LOCATION_INPUT, event_data.location)
        
        if event_data.reminder_minutes:
            self.select_reminder(event_data.reminder_minutes)
        
        if event_data.is_recurring:
            self.set_recurring(event_data.is_recurring)
            if event_data.recurrence_pattern:
                self.select_recurrence_pattern(event_data.recurrence_pattern)
    
    @allure.step("Выбрать напоминание: {minutes} минут")
    def select_reminder(self, minutes: int) -> None:
        """
        Выбрать время напоминания.
        
        Args:
            minutes: Минуты до события
        """
        select = Select(self.find_element(self.EVENT_REMINDER_SELECT))
        select.select_by_value(str(minutes))
    
    @allure.step("Установить повторяющееся событие: {is_recurring}")
    def set_recurring(self, is_recurring: bool) -> None:
        """
        Установить флаг повторяющегося события.
        
        Args:
            is_recurring: True для повторяющегося события
        """
        checkbox = self.find_element(self.EVENT_RECURRING_CHECKBOX)
        if is_recurring != checkbox.is_selected():
            checkbox.click()
    
    @allure.step("Выбрать паттерн повторения: {pattern}")
    def select_recurrence_pattern(self, pattern: str) -> None:
        """
        Выбрать паттерн повторения события.
        
        Args:
            pattern: Паттерн повторения (DAILY, WEEKLY, MONTHLY)
        """
        if self.is_visible(self.EVENT_RECURRENCE_PATTERN_SELECT):
            select = Select(self.find_element(self.EVENT_RECURRENCE_PATTERN_SELECT))
            select.select_by_value(pattern)
    
    @allure.step("Сохранить событие")
    def save_event(self) -> None:
        """Сохранить событие."""
        self.click(self.SAVE_EVENT_BUTTON)
        self.wait_for_page_load()
    
    @allure.step("Создать новое событие")
    def create_event(self, event_data: EventData) -> None:
        """
        Создать новое событие.
        
        Args:
            event_data: Данные события
        """
        self.click_create_event()
        self.fill_event_form(event_data)
        self.save_event()
    
    @allure.step("Получить количество событий")
    def get_events_count(self) -> int:
        """
        Получить количество отображаемых событий.
        
        Returns:
            Количество событий
        """
        events = self.find_elements(self.EVENT_LIST, timeout=5)
        return len(events)
    
    @allure.step("Получить список заголовков событий")
    def get_event_titles(self) -> List[str]:
        """
        Получить список заголовков всех событий.
        
        Returns:
            Список заголовков
        """
        titles = []
        events = self.find_elements(self.EVENT_TITLE, timeout=5)
        for event in events:
            titles.append(event.text.strip())
        return titles
    
    @allure.step("Найти событие по заголовку: {title}")
    def find_event_by_title(self, title: str) -> Optional[Tuple[int, "WebElement"]]:
        """
        Найти событие по заголовку.
        
        Args:
            title: Заголовок события
            
        Returns:
            Кортеж (индекс, элемент) или None
        """
        events = self.find_elements(self.EVENT_LIST, timeout=5)
        for idx, event in enumerate(events):
            try:
                event_title = event.find_element(*self.EVENT_TITLE).text.strip()
                if event_title == title:
                    return idx, event
            except:
                continue
        return None
    
    @allure.step("Редактировать событие: {title}")
    def edit_event(self, old_title: str, new_data: EventData) -> bool:
        """
        Редактировать существующее событие.
        
        Args:
            old_title: Заголовок редактируемого события
            new_data: Новые данные события
            
        Returns:
            True если событие отредактировано, иначе False
        """
        result = self.find_event_by_title(old_title)
        if not result:
            return False
        
        idx, event = result
        # Открыть действия события
        actions_button = event.find_element(*self.EVENT_ACTIONS)
        actions_button.click()
        
        # Нажать редактировать
        self.click(self.EDIT_EVENT_BUTTON)
        
        # Заполнить форму
        self.fill_event_form(new_data)
        self.save_event()
        
        return True
    
    @allure.step("Удалить событие: {title}")
    def delete_event(self, title: str) -> bool:
        """
        Удалить событие.
        
        Args:
            title: Заголовок удаляемого события
            
        Returns:
            True если событие удалено, иначе False
        """
        result = self.find_event_by_title(title)
        if not result:
            return False
        
        idx, event = result
        # Открыть действия события
        actions_button = event.find_element(*self.EVENT_ACTIONS)
        actions_button.click()
        
        # Нажать удалить
        self.click(self.DELETE_EVENT_BUTTON)
        
        # Подтвердить удаление в модальном окне
        if self.is_visible(self.CONFIRM_DELETE_MODAL, timeout=5):
            self.click(self.CONFIRM_DELETE_BUTTON)
        
        self.wait_for_page_load()
        return True
    
    @allure.step("Поиск событий по тексту: {search_text}")
    def search_events(self, search_text: str) -> None:
        """
        Поиск событий по тексту.
        
        Args:
            search_text: Текст для поиска
        """
        self.type_text(self.SEARCH_INPUT, search_text)
        # Нажать Enter для поиска
        self.find_element(self.SEARCH_INPUT).send_keys("\n")
        self.wait_for_page_load()
    
    @allure.step("Применить фильтры")
    def apply_filters(self, date_filter: Optional[str] = None, status_filter: Optional[str] = None) -> None:
        """
        Применить фильтры к списку событий.
        
        Args:
            date_filter: Фильтр по дате
            status_filter: Фильтр по статусу
        """
        if date_filter and self.is_visible(self.DATE_FILTER):
            select = Select(self.find_element(self.DATE_FILTER))
            select.select_by_value(date_filter)
        
        if status_filter and self.is_visible(self.STATUS_FILTER):
            select = Select(self.find_element(self.STATUS_FILTER))
            select.select_by_value(status_filter)
        
        if self.is_visible(self.APPLY_FILTERS_BUTTON):
            self.click(self.APPLY_FILTERS_BUTTON)
            self.wait_for_page_load()
    
    @allure.step("Очистить фильтры")
    def clear_filters(self) -> None:
        """Очистить все примененные фильтры."""
        if self.is_visible(self.CLEAR_FILTERS_BUTTON):
            self.click(self.CLEAR_FILTERS_BUTTON)
            self.wait_for_page_load()
    
    @allure.step("Проверить наличие сообщения 'Нет событий'")
    def is_no_events_message_displayed(self) -> bool:
        """
        Проверить отображение сообщения об отсутствии событий.
        
        Returns:
            True если сообщение отображается, иначе False
        """
        return self.is_visible(self.NO_EVENTS_MESSAGE, timeout=5)
    
    @allure.step("Проверить успешное создание события")
    def is_event_created_successfully(self) -> bool:
        """
        Проверить успешное создание события.
        
        Returns:
            True если уведомление об успехе отображается, иначе False
        """
        return self.is_visible(self.SUCCESS_NOTIFICATION, timeout=5)
    
    @allure.step("Получить текст уведомления об успехе")
    def get_success_message(self) -> Optional[str]:
        """
        Получить текст уведомления об успехе.
        
        Returns:
            Текст уведомления или None
        """
        if self.is_visible(self.SUCCESS_NOTIFICATION, timeout=5):
            return self.get_text(self.SUCCESS_NOTIFICATION)
        return None
