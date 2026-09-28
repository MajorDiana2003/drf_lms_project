from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def check_inactive_users():
    """Периодическая задача для блокировки пользователей, неактивных более месяца."""
    month_ago = timezone.now() - timedelta(days=30)

    # Ищем всех активных пользователей, которые не заходили более 30 дней
    # Поле last_login__isnull=False страхует от блокировки только что созданных юзеров
    inactive_users = User.objects.filter(
        last_login__lt=month_ago, last_login__isnull=False, is_active=True
    )

    count = inactive_users.count()

    if count > 0:
        # Критерий ТЗ: Обновление происходит батчем (.update()), а не в цикле по одному
        inactive_users.update(is_active=False)
        print(f"Батч-обновление успешно: заблокировано {count} пользователей.")
    else:
        print("Неактивных пользователей для блокировки не найдено.")
