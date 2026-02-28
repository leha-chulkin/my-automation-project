"""
API клиент для работы с личными событиями в Авиасейлс.
"""
import allure
import logging
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
from requests.exceptions import RequestException, Timeout

from config.settings import settings
from config.test_data import EventData


@dataclass
class EventResponse:
    """Ответ от API событий."""
    success: bool
    event_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    status_code: Optional[int] = None
    error: Optional[str] = None


@dataclass
class EventsListResponse:
    """Ответ со списком событий."""
    success: bool
    events: List[Dict[str, Any]] = None
    total: int = 0
    message: Optional[str] = None
    status_code: Optional[int] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.events is None:
            self.events = []


class EventsAPI:
    """Клиент для работы с API личных событий."""
    
    def __init__(self, auth_token: Optional[str] = None):
        self.base_url = settings.api_base_url
        self.timeout = settings.api_timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Настройка сессии
        self.session.headers.update({
            'User-Agent': 'Aviasales-Testing/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        if auth_token:
            self.set_auth_token(auth_token)
    
    def set_auth_token(self, token: str) -> None:
        """
        Установить токен авторизации.
        
        Args:
            token: Токен авторизации
        """
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def _format_datetime(self, dt: datetime) -> str:
        """
        Форматировать datetime для API.
        
        Args:
            dt: Объект datetime
            
        Returns:
            Отформатированная строка
        """
        return dt.isoformat()
    
    def _event_to_payload(self, event_data: EventData) -> Dict[str, Any]:
        """
        Конвертировать EventData в payload для API.
        
        Args:
            event_data: Данные события
            
        Returns:
            Словарь с данными события
        """
        payload = {
            'title': event_data.title,
            'description': event_data.description,
            'start_date': self._format_datetime(event_data.start_date),
            'end_date': self._format_datetime(event_data.end_date),
            'location': event_data.location,
            'reminder_minutes': event_data.reminder_minutes,
            'is_recurring': event_data.is_recurring
        }
        
        if event_data.recurrence_pattern:
            payload['recurrence_pattern'] = event_data.recurrence_pattern
        
        return payload
    
    @allure.step("API: Создание события '{title}'")
    def create_event(self, event_data: EventData) -> EventResponse:
        """
        Создать новое личное событие через API.
        
        Args:
            event_data: Данные события
            
        Returns:
            EventResponse с результатом создания
        """
        url = f"{self.base_url}/api/v1/events"
        payload = self._event_to_payload(event_data)
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            self.logger.info(f"Создание события: {event_data.title}, статус: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                return EventResponse(
                    success=True,
                    event_id=data.get('id'),
                    data=data,
                    message='Событие создано успешно',
                    status_code=response.status_code
                )
            else:
                error_data = response.json() if response.content else {}
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка создания события'),
                    message=error_data.get('message')
                )
                
        except Timeout:
            self.logger.error(f"Таймаут при создании события: {event_data.title}")
            return EventResponse(
                success=False,
                error="Таймаут соединения",
                message="Превышено время ожидания ответа от сервера"
            )
        except RequestException as e:
            self.logger.error(f"Ошибка сети при создании события: {str(e)}")
            return EventResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Получение события по ID: {event_id}")
    def get_event(self, event_id: str) -> EventResponse:
        """
        Получить событие по ID.
        
        Args:
            event_id: ID события
            
        Returns:
            EventResponse с данными события
        """
        url = f"{self.base_url}/api/v1/events/{event_id}"
        
        try:
            response = self.session.get(
                url,
                timeout=self.timeout
            )
            
            self.logger.info(f"Получение события {event_id}, статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return EventResponse(
                    success=True,
                    event_id=event_id,
                    data=data,
                    message='Событие получено успешно',
                    status_code=response.status_code
                )
            elif response.status_code == 404:
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error='Событие не найдено'
                )
            else:
                error_data = response.json() if response.content else {}
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка получения события'),
                    message=error_data.get('message')
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при получении события {event_id}: {str(e)}")
            return EventResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Обновление события {event_id}")
    def update_event(self, event_id: str, event_data: EventData) -> EventResponse:
        """
        Обновить существующее событие.
        
        Args:
            event_id: ID события
            event_data: Новые данные события
            
        Returns:
            EventResponse с результатом обновления
        """
        url = f"{self.base_url}/api/v1/events/{event_id}"
        payload = self._event_to_payload(event_data)
        
        try:
            response = self.session.put(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            self.logger.info(f"Обновление события {event_id}, статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return EventResponse(
                    success=True,
                    event_id=event_id,
                    data=data,
                    message='Событие обновлено успешно',
                    status_code=response.status_code
                )
            elif response.status_code == 404:
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error='Событие не найдено'
                )
            else:
                error_data = response.json() if response.content else {}
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка обновления события'),
                    message=error_data.get('message')
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении события {event_id}: {str(e)}")
            return EventResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Удаление события {event_id}")
    def delete_event(self, event_id: str) -> EventResponse:
        """
        Удалить событие по ID.
        
        Args:
            event_id: ID события
            
        Returns:
            EventResponse с результатом удаления
        """
        url = f"{self.base_url}/api/v1/events/{event_id}"
        
        try:
            response = self.session.delete(
                url,
                timeout=self.timeout
            )
            
            self.logger.info(f"Удаление события {event_id}, статус: {response.status_code}")
            
            if response.status_code == 204:
                return EventResponse(
                    success=True,
                    message='Событие удалено успешно',
                    status_code=response.status_code
                )
            elif response.status_code == 404:
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error='Событие не найдено'
                )
            else:
                error_data = response.json() if response.content else {}
                return EventResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка удаления события'),
                    message=error_data.get('message')
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при удалении события {event_id}: {str(e)}")
            return EventResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Получение списка событий")
    def get_events(
        self,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> EventsListResponse:
        """
        Получить список личных событий с фильтрацией.
        
        Args:
            limit: Количество событий
            offset: Смещение
            search: Поисковый запрос
            start_date: Начальная дата фильтра
            end_date: Конечная дата фильтра
            
        Returns:
            EventsListResponse со списком событий
        """
        url = f"{self.base_url}/api/v1/events"
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if search:
            params['search'] = search
        
        if start_date:
            params['start_date'] = self._format_datetime(start_date)
        
        if end_date:
            params['end_date'] = self._format_datetime(end_date)
        
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            self.logger.info(f"Получение списка событий, статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return EventsListResponse(
                    success=True,
                    events=data.get('events', []),
                    total=data.get('total', 0),
                    message='Список событий получен успешно',
                    status_code=response.status_code
                )
            else:
                error_data = response.json() if response.content else {}
                return EventsListResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка получения списка событий'),
                    message=error_data.get('message')
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при получении списка событий: {str(e)}")
            return EventsListResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Поиск событий по заголовку")
    def search_events_by_title(self, title: str) -> EventsListResponse:
        """
        Поиск событий по заголовку.
        
        Args:
            title: Заголовок для поиска
            
        Returns:
            EventsListResponse с найденными событиями
        """
        return self.get_events(search=title)
    
    @allure.step("API: Получение предстоящих событий")
    def get_upcoming_events(self, days: int = 7) -> EventsListResponse:
        """
        Получить предстоящие события.
        
        Args:
            days: Количество дней вперед
            
        Returns:
            EventsListResponse с предстоящими событиями
        """
        start_date = datetime.now()
        end_date = datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=days)
        
        return self.get_events(start_date=start_date, end_date=end_date)
    
    @allure.step("API: Проверка существования события по заголовку")
    def event_exists(self, title: str) -> bool:
        """
        Проверить существование события по заголовку.
        
        Args:
            title: Заголовок события
            
        Returns:
            True если событие существует, иначе False
        """
        response = self.search_events_by_title(title)
        if response.success and response.events:
            for event in response.events:
                if event.get('title') == title:
                    return True
        return False
    
    @allure.step("API: Получение события по заголовку")
    def get_event_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Получить событие по заголовку.
        
        Args:
            title: Заголовок события
            
        Returns:
            Данные события или None
        """
        response = self.search_events_by_title(title)
        if response.success and response.events:
            for event in response.events:
                if event.get('title') == title:
                    return event
        return None