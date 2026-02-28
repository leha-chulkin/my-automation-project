"""
API клиент для авторизации в Авиасейлс.
"""
import allure
import logging
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from requests.exceptions import RequestException, Timeout

from config.settings import settings
from config.test_data import UserData


@dataclass
class AuthResponse:
    """Ответ от API авторизации."""
    success: bool
    token: Optional[str] = None
    user_id: Optional[str] = None
    message: Optional[str] = None
    status_code: Optional[int] = None
    error: Optional[str] = None


class AuthAPI:
    """Клиент для работы с API авторизации."""
    
    def __init__(self):
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
    
    @allure.step("API: Авторизация пользователя {email}")
    def login(self, email: str, password: str) -> AuthResponse:
        """
        Авторизация пользователя через API.
        
        Args:
            email: Email пользователя
            password: Пароль пользователя
            
        Returns:
            AuthResponse с результатом авторизации
        """
        url = f"{self.base_url}/api/v1/auth/login"
        payload = {
            'email': email,
            'password': password
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            self.logger.info(f"Авторизация: {email}, статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return AuthResponse(
                    success=True,
                    token=data.get('token'),
                    user_id=data.get('user_id'),
                    message=data.get('message', 'Авторизация успешна'),
                    status_code=response.status_code
                )
            else:
                error_data = response.json() if response.content else {}
                return AuthResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка авторизации'),
                    message=error_data.get('message')
                )
                
        except Timeout:
            self.logger.error(f"Таймаут при авторизации: {email}")
            return AuthResponse(
                success=False,
                error="Таймаут соединения",
                message="Превышено время ожидания ответа от сервера"
            )
        except RequestException as e:
            self.logger.error(f"Ошибка сети при авторизации: {str(e)}")
            return AuthResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при авторизации: {str(e)}")
            return AuthResponse(
                success=False,
                error="Внутренняя ошибка",
                message=str(e)
            )
    
    @allure.step("API: Авторизация с данными пользователя")
    def login_with_user_data(self, user_data: UserData) -> AuthResponse:
        """
        Авторизация с использованием объекта UserData.
        
        Args:
            user_data: Данные пользователя
            
        Returns:
            AuthResponse с результатом авторизации
        """
        return self.login(user_data.email, user_data.password)
    
    @allure.step("API: Выход из системы")
    def logout(self, token: str) -> AuthResponse:
        """
        Выход из системы через API.
        
        Args:
            token: Токен авторизации
            
        Returns:
            AuthResponse с результатом выхода
        """
        url = f"{self.base_url}/api/v1/auth/logout"
        headers = {'Authorization': f'Bearer {token}'}
        
        try:
            response = self.session.post(
                url,
                headers=headers,
                timeout=self.timeout
            )
            
            self.logger.info(f"Выход из системы, статус: {response.status_code}")
            
            if response.status_code == 200:
                return AuthResponse(
                    success=True,
                    message='Выход выполнен успешно',
                    status_code=response.status_code
                )
            else:
                return AuthResponse(
                    success=False,
                    status_code=response.status_code,
                    error='Ошибка выхода из системы'
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при выходе из системы: {str(e)}")
            return AuthResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Проверка токена")
    def validate_token(self, token: str) -> AuthResponse:
        """
        Проверка валидности токена авторизации.
        
        Args:
            token: Токен для проверки
            
        Returns:
            AuthResponse с результатом проверки
        """
        url = f"{self.base_url}/api/v1/auth/validate"
        headers = {'Authorization': f'Bearer {token}'}
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            
            self.logger.info(f"Проверка токена, статус: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return AuthResponse(
                    success=True,
                    user_id=data.get('user_id'),
                    message='Токен валиден',
                    status_code=response.status_code
                )
            else:
                return AuthResponse(
                    success=False,
                    status_code=response.status_code,
                    error='Токен невалиден'
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при проверке токена: {str(e)}")
            return AuthResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Получение информации о пользователе")
    def get_user_info(self, token: str) -> Dict[str, Any]:
        """
        Получение информации о текущем пользователе.
        
        Args:
            token: Токен авторизации
            
        Returns:
            Словарь с информацией о пользователе
        """
        url = f"{self.base_url}/api/v1/auth/user"
        headers = {'Authorization': f'Bearer {token}'}
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Ошибка получения информации о пользователе: {response.status_code}")
                return {}
                
        except Exception as e:
            self.logger.error(f"Ошибка при получении информации о пользователе: {str(e)}")
            return {}
    
    @allure.step("API: Обновление токена")
    def refresh_token(self, refresh_token: str) -> AuthResponse:
        """
        Обновление токена авторизации.
        
        Args:
            refresh_token: Refresh токен
            
        Returns:
            AuthResponse с новым токеном
        """
        url = f"{self.base_url}/api/v1/auth/refresh"
        payload = {'refresh_token': refresh_token}
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return AuthResponse(
                    success=True,
                    token=data.get('token'),
                    message='Токен обновлен',
                    status_code=response.status_code
                )
            else:
                return AuthResponse(
                    success=False,
                    status_code=response.status_code,
                    error='Ошибка обновления токена'
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении токена: {str(e)}")
            return AuthResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )
    
    @allure.step("API: Регистрация нового пользователя")
    def register(self, user_data: UserData) -> AuthResponse:
        """
        Регистрация нового пользователя через API.
        
        Args:
            user_data: Данные пользователя
            
        Returns:
            AuthResponse с результатом регистрации
        """
        url = f"{self.base_url}/api/v1/auth/register"
        payload = {
            'email': user_data.email,
            'password': user_data.password,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'phone': user_data.phone
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            self.logger.info(f"Регистрация: {user_data.email}, статус: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                return AuthResponse(
                    success=True,
                    token=data.get('token'),
                    user_id=data.get('user_id'),
                    message='Регистрация успешна',
                    status_code=response.status_code
                )
            else:
                error_data = response.json() if response.content else {}
                return AuthResponse(
                    success=False,
                    status_code=response.status_code,
                    error=error_data.get('error', 'Ошибка регистрации'),
                    message=error_data.get('message')
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при регистрации: {str(e)}")
            return AuthResponse(
                success=False,
                error="Ошибка сети",
                message=str(e)
            )