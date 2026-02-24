# Automation Project

## Описание
В этом репозитории реализованы UI‑ и API‑тесты для проекта **[название финального проекта]**.  
Тесты написаны с использованием `pytest`, `selenium`, `requests` и `allure`.

## Структура
automation-project/
├── config/ # настройки и секреты
├── pages/ # Page‑Object модели
├── api/ # API‑обёртка
├── tests/ # тесты (UI + API)
├── requirements.txt
├── pytest.ini
├── README.md


## Установка зависимостей
```bash
pip install -r requirements.txt
Запуск тестов
1️⃣ UI‑тесты
pytest -m ui
2️⃣ API‑тесты
pytest -m api
3️⃣ Все тесты
pytest
4️⃣ Генерация отчёта Allure
pytest --alluredir=allure-results
allure serve allure-results
Конфигурация
Создайте файл .env в корне проекта (не добавляйте его в Git) с переменными:

BASE_URL=https://example.com
API_BASE_URL=https://example.com/api
TIMEOUT=10
LOGIN_EMAIL=test@example.com
LOGIN_PASSWORD=SuperSecret123
API_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Линтинг
black --check .
flake8 .
isort --check-only .
Финальный проект
Ссылка на ручной тестовый проект: [URL]

Автор: <ваше имя>


---

## 📌 Как проверить, что всё работает

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить UI‑тесты
pytest -m ui

# Запустить API‑тесты
pytest -m api

# Запустить все тесты
pytest

# Сгенерировать отчёт Allure
pytest --alluredir=allure-results
allure serve allure-results