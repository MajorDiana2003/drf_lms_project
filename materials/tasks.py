from celery import shared_task
from django.core.mail import send_mail
from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Асинхронная задача для отправки уведомлений об обновлении курса."""
    try:
        course = Course.objects.get(pk=course_id)
        # Получаем всех пользователей, подписанных на этот курс
        subscriptions = Subscription.objects.filter(course=course)
        recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

        if recipient_list:
            send_mail(
                subject=f"Обновление курса: {course.title}",
                message=(
                    f"Здравствуйте! Материалы курса '{course.title}' были "
                    "успешно обновлены. Заходите на платформу, чтобы "
                    "изучить новые материалы."
                ),
                from_email="no-reply@lms-platform.ru",
                recipient_list=recipient_list,
                fail_silently=False,
            )
            print(f"Уведомления успешно отправлены для {len(recipient_list)} пользователей.")
    except Course.DoesNotExist:
        print(f"Курс с id={course_id} не найден.")
