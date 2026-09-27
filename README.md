# DRF LMS Project 

Веб-приложение для управления обучением (LMS) с использованием Django REST Framework.

## Стек технологий
- Python 3.12+
- Django 5.x
- Django REST Framework (DRF)
- Pillow (для работы с изображениями)
- Flake8 (линтер кода)

## Как запустить проект локально

1. **Клонируйте репозиторий и перейдите в ветку домашней работы:**
   ```bash
   git clone <ссылка_на_ваш_репозиторий>
   cd drf_lms_project
   git checkout feature/homework_30.1
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   ```
**Настройте переменные окружения:**
   - Скопируйте шаблон файла конфигурации:
     ```bash
     cp env.example .env
     ```
     *(Если вы на Windows в PowerShell, используйте команду: `cp env.example .env` или вручную переименуйте скопированный файл в `.env`)*
   - Откройте созданный файл `.env` и укажите в переменной `SECRET_KEY` ваш секретный ключ Django.

**Установите все зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Примените миграции базы данных:**
   ```bash
   python manage.py migrate
   ```

5. **Создайте суперпользователя (администратора):**
   ```bash
   python manage.py createsuperuser
   ```
   *Система попросит ввести Email и пароль (авторизация по умолчанию настроена через Email).*

6. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```
   Проект будет доступен по адресу: `http://127.0.0`

## Проверка качества кода
Для запуска линтера кода выполните команду в корне проекта:
```bash
flake8 .
```

##                            *Лицензия*
Проект распространяется под  **[Apache License]**
