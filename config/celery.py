import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('drf_lms')

# Настройки Celery будут браться из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматический поиск задач во всех установленных приложениях
app.autodiscover_tasks()
