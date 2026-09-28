from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/course_previews/",
        verbose_name="Превью (картинка)",
        blank=True,
        null=True,
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        blank=True,
        null=True,
        help_text="Введите описание урока",
    )
    preview = models.ImageField(
        upload_to="materials/lesson_previews/",
        verbose_name="Превью (картинка)",
        blank=True,
        null=True,
        help_text="Загрузите превью урока",
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Укажите ссылку на видео-урок",
    )

    # Связь: у одного курса может быть много уроков
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
        help_text="Выберите курс, к которому относится урок",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
