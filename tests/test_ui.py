"""
UI тесты для функционала "Личные события" Авиасейлс.
"""
import pytest
import allure
from typing import Optional

from config.test_data import TestData
from pages.login_page import LoginPage
from pages.personal_events_page import PersonalEventsPage


@allure.epic("Авиасейлс - Личные события")
@allure.feature("UI тестирование")
class TestPersonalEventsUI:
    """Класс UI тестов для личных событий."""
    
    @allure.story("Авторизация")
    @allure.title("Успешная авторизация валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, login_page: LoginPage, test_data: TestData):
        """
        Тест успешной авторизации с валидными данными.
        
        Steps:
        1. Открыть страницу авторизации
        2. Ввести валидный email
        3. Ввести валидный пароль
        4. Нажать кнопку "Войти"
        5. Проверить успешную авторизацию
        
        Expected:
        Пользователь успешно авторизован, отображается меню пользователя
        """
        with allure.step("Открыть страницу авторизации"):
            login_page.open_login_page()
            assert login_page.is_login_form_displayed(), "Форма авторизации не отображается"
        
        with allure.step("Выполнить авторизацию с валидными данными"):
            login_page.login_with_user_data(test_data.VALID_USER)
        
        with allure.step("Проверить успешную авторизацию"):
            assert login_page.is_login_successful(), "Авторизация не выполнена успешно"
    
    @allure.story("Авторизация")
    @allure.title("Неуспешная авторизация невалидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_failed_login_invalid_credentials(self, login_page: LoginPage, test_data: TestData):
        """
        Тест неуспешной авторизации с невалидными данными.
        
        Steps:
        1. Открыть страницу авторизации
        2. Ввести невалидный email
        3. Ввести невалидный пароль
        4. Нажать кнопку "Войти"
        5. Проверить отображение ошибки
        
        Expected:
        Отображается сообщение об ошибке авторизации
        """
        with allure.step("Открыть страницу авторизации"):
            login_page.open_login_page()
        
        with allure.step("Выполнить авторизацию с невалидными данными"):
            login_page.login_with_user_data(test_data.INVALID_USER)
        
        with allure.step("Проверить отображение ошибки"):
            assert login_page.is_error_displayed(), "Ошибка авторизации не отображается"
            error_message = login_page.get_error_message()
            assert error_message, "Текст ошибки не получен"
            allure.attach(f"Текст ошибки: {error_message}", name="Error Message")
    
    @allure.story("Создание событий")
    @allure.title("Создание нового личного события")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.usefixtures("authenticated_events_page")
    def test_create_personal_event(
        self,
        authenticated_events_page: PersonalEventsPage,
        data_generator,
        cleanup_events
    ):
        """
        Тест создания нового личного события.
        
        Steps:
        1. Открыть страницу личных событий
        2. Нажать кнопку "Создать событие"
        3. Заполнить форму данными события
        4. Сохранить событие
        5. Проверить успешное создание
        
        Expected:
        Событие успешно создано, отображается в списке событий
        """
        # Генерация тестовых данных
        event_data = data_generator.generate_event(title="Тестовое событие UI")
        
        with allure.step("Открыть страницу личных событий"):
            authenticated_events_page.open_events_page()
            assert authenticated_events_page.is_events_section_displayed(), \
                "Раздел личных событий не отображается"
        
        with allure.step("Создать новое событие"):
            initial_count = authenticated_events_page.get_events_count()
            authenticated_events_page.create_event(event_data)
        
        with allure.step("Проверить успешное создание события"):
            assert authenticated_events_page.is_event_created_successfully(), \
                "Уведомление об успешном создании не отображается"
            
            # Проверить увеличение количества событий
            final_count = authenticated_events_page.get_events_count()
            assert final_count == initial_count + 1, \
                f"Количество событий не увеличилось. Было: {initial_count}, стало: {final_count}"
            
            # Проверить наличие события в списке
            event_titles = authenticated_events_page.get_event_titles()
            assert event_data.title in event_titles, \
                f"Событие '{event_data.title}' не найдено в списке"
    
    @allure.story("Редактирование событий")
    @allure.title("Редактирование существующего события")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.usefixtures("authenticated_events_page")
    def test_edit_personal_event(
        self,
        authenticated_events_page: PersonalEventsPage,
        create_test_event,
        data_generator,
        cleanup_events
    ):
        """
        Тест редактирования существующего личного события.
        
        Steps:
        1. Создать тестовое событие через API
        2. Открыть страницу личных событий
        3. Найти созданное событие
        4. Открыть форму редактирования
        5. Изменить данные события
        6. Сохранить изменения
        7. Проверить обновление события
        
        Expected:
        Событие успешно отредактировано, данные обновлены
        """
        # Создание тестового события через API
        event_id, original_event = create_test_event()
        assert event_id, "Не удалось создать тестовое событие"
        
        # Генерация новых данных для события
        updated_event = data_generator.generate_event(title="Обновленное событие UI")
        
        with allure.step("Открыть страницу личных событий"):
            authenticated_events_page.open_events_page()
        
        with allure.step("Редактировать существующее событие"):
            result = authenticated_events_page.edit_event(
                original_event.title,
                updated_event
            )
            assert result, f"Не удалось найти событие '{original_event.title}' для редактирования"
        
        with allure.step("Проверить обновление события"):
            # Обновить список событий
            authenticated_events_page.refresh_page()
            
            # Проверить, что старое название отсутствует
            event_titles = authenticated_events_page.get_event_titles()
            assert original_event.title not in event_titles, \
                f"Старое событие '{original_event.title}' все еще отображается"
            
            # Проверить, что новое название присутствует
            assert updated_event.title in event_titles, \
                f"Обновленное событие '{updated_event.title}' не найдено в списке"
    
    @allure.story("Удаление событий")
    @allure.title("Удаление личного события")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.usefixtures("authenticated_events_page")
    def test_delete_personal_event(
        self,
        authenticated_events_page: PersonalEventsPage,
        create_test_event,
        cleanup_events
    ):
        """
        Тест удаления личного события.
        
        Steps:
        1. Создать тестовое событие через API
        2. Открыть страницу личных событий
        3. Найти созданное событие
        4. Удалить событие
        5. Подтвердить удаление
        6. Проверить удаление события
        
        Expected:
        Событие успешно удалено, отсутствует в списке событий
        """
        # Создание тестового события через API
        event_id, event_data = create_test_event()
        assert event_id, "Не удалось создать тестовое событие"
        
        with allure.step("Открыть страницу личных событий"):
            authenticated_events_page.open_events_page()
            initial_count = authenticated_events_page.get_events_count()
        
        with allure.step("Удалить событие"):
            result = authenticated_events_page.delete_event(event_data.title)
            assert result, f"Не удалось найти событие '{event_data.title}' для удаления"
        
        with allure.step("Проверить удаление события"):
            # Обновить список событий
            authenticated_events_page.refresh_page()
            
            # Проверить уменьшение количества событий
            final_count = authenticated_events_page.get_events_count()
            assert final_count == initial_count - 1, \
                f"Количество событий не уменьшилось. Было: {initial_count}, стало: {final_count}"
            
            # Проверить отсутствие события в списке
            event_titles = authenticated_events_page.get_event_titles()
            assert event_data.title not in event_titles, \
                f"Удаленное событие '{event_data.title}' все еще отображается"
    
    @allure.story("Поиск и фильтрация")
    @allure.title("Поиск событий по заголовку")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.usefixtures("authenticated_events_page")
    def test_search_events(
        self,
        authenticated_events_page: PersonalEventsPage,
        create_test_event,
        data_generator,
        cleanup_events
    ):
        """
        Тест поиска событий по заголовку.
        
        Steps:
        1. Создать несколько тестовых событий
        2. Открыть страницу личных событий
        3. Ввести текст для поиска
        4. Проверить результаты поиска
        
        Expected:
        Отображаются только события, соответствующие поисковому запросу
        """
        # Создание тестовых событий
        search_term = "УникальныйПоиск"
        event1 = data_generator.generate_event(title=f"{search_term} Событие 1")
        event2 = data_generator.generate_event(title="Обычное Событие 2")
        event3 = data_generator.generate_event(title=f"{searchTerm} Событие 3")
        
        for event in [event1, event2, event3]:
            create_test_event(event)
        
        with allure.step("Открыть страницу личных событий"):
            authenticated_events_page.open_events_page()
            total_events = authenticated_events_page.get_events_count()
        
        with allure.step("Выполнить поиск событий"):
            authenticated_events_page.search_events(search_term)
        
        with allure.step("Проверить результаты поиска"):
            # Получить список найденных событий
            found_titles = authenticated_events_page.get_event_titles()
            
            # Проверить, что найдены только события с search_term
            for title in found_titles:
                assert search_term in title, \
                    f"Найдено событие без поискового запроса: {title}"
            
            # Проверить, что количество найденных событий меньше общего количества
            found_count = len(found_titles)
            assert found_count < total_events, \
                f"Найдены все события ({found_count}), поиск не работает"
            
            allure.attach(
                f"Найдено {found_count} из {total_events} событий",
                name="Search Results"
            )
    
    @allure.story("Валидация данных")
    @allure.title("Создание события с пустым заголовком")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.usefixtures("authenticated_events_page")
    def test_create_event_empty_title(
        self,
        authenticated_events_page: PersonalEventsPage,
        data_generator,
        cleanup_events
    ):
        """
        Тест создания события с пустым заголовком.
        
        Steps:
        1. Открыть страницу личных событий
        2. Нажать кнопку "Создать событие"
        3. Заполнить форму с пустым заголовком
        4. Попытаться сохранить событие
        5. Проверить отображение ошибки валидации
        
        Expected:
        Отображается ошибка валидации, событие не создано
        """
        # Создание события с пустым заголовком
        event_data = data_generator.generate_event()
        event_data.title = ""
        
        with allure.step("Открыть страницу личных событий"):
            authenticated_events_page.open_events_page()
            initial_count = authenticated_events_page.get_events_count()
        
        with allure.step("Попытаться создать событие с пустым заголовком"):
            authenticated_events_page.create_event(event_data)
        
        with allure.step("Проверить отображение ошибки валидации"):
            # Проверить, что количество событий не изменилось
            final_count = authenticated_events_page.get_events_count()
            assert final_count == initial_count, \
                f"Событие создано несмотря на пустой заголовок. Было: {initial_count}, стало: {final_count}"
            
            # Проверить отображение ошибки (если есть соответствующее поле)
            # Это зависит от реализации фронтенда
    
    @allure.story("Навигация")
    @allure.title("Доступ к личным событиям без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_access_events_without_auth(self, driver, base_url):
        """
        Тест доступа к странице личных событий без авторизации.
        
        Steps:
        1. Открыть страницу личных событий без авторизации
        2. Проверить редирект на страницу авторизации
        
        Expected:
        Пользователь перенаправлен на страницу авторизации
        """
        page = PersonalEventsPage(driver)
        page.base_url = base_url
        
        with allure.step("Открыть страницу личных событий без авторизации"):
            page.open_events_page()
        
        with allure.step("Проверить редирект на авторизацию"):
            current_url = page.get_current_url()
            assert "/login" in current_url or "/auth" in current_url, \
                f"Не произошел редирект на авторизацию. Текущий URL: {current_url}"
    
    @allure.story("Производительность")
    @allure.title("Быстрая навигация по событиям")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.usefixtures("authenticated_events_page")
    def test_fast_navigation_between_events(
        self,
        authenticated_events_page: PersonalEventsPage,
        create_test_event,
        data_generator,
        cleanup_events
    ):
        """
        Тест быстрой навигации между событиями.
        
        Steps:
        1. Создать несколько событий
        2. Открыть страницу личных событий
        3. Быстро выполнить несколько операций
        
        Expected:
        Все операции выполняются быстро, без задержек
        """
        # Создание нескольких событий
        events = []
        for i in range(3):
            event = data_generator.generate_event(title=f"Событие для навигации {i}")
            create_test_event(event)
            events.append(event)
        
        with allure.step("Открыть страницу личных событий"):
            authenticated_events_page.open_events_page()
        
        with allure.step("Выполнить быстрые операции"):
            # Проверить отображение всех событий
            event_titles = authenticated_events_page.get_event_titles()
            for event in events:
                assert event.title in event_titles, \
                    f"Событие '{event.title}' не отображается"
            
            # Выполнить поиск
            authenticated_events_page.search_events("навигации")
            
            # Очистить поиск
            authenticated_events_page.clear_filters()
            
            # Проверить, что все события снова отображаются
            final_titles = authenticated_events_page.get_event_titles()
            assert len(final_titles) >= len(events), \
                f"После очистки фильтров отображается меньше событий: {len(final_titles)}"
