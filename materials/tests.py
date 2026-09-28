from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from materials.models import Course, Lesson, Subscription
from users.models import User


class MaterialsTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей разных групп
        self.user = User.objects.create(email="user@example.com")
        self.user.set_password("password123")
        self.user.save()

        self.moderator = User.objects.create(email="moder@example.com")
        self.moderator.set_password("password123")
        self.moderator.save()

        # Добавляем модератора в группу
        self.moder_group, _ = Group.objects.get_or_create(name="модераторы")
        self.moderator.groups.add(self.moder_group)

        # Создаем базовые сущности
        self.course = Course.objects.create(title="Django Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="DRF Intro",
            video_url="https://youtube.com",
            course=self.course,
            owner=self.user
        )

    def test_lesson_create(self):
        """Тест создания урока авторизованным пользователем и валидация ссылки"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-create')

        # Корректная ссылка на youtube
        data = {"title": "New Lesson", "video_url": "https://youtube.com", "course": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Некорректная ссылка на сторонний ресурс
        invalid_data = {"title": "Bad Lesson", "video_url": "https://wikipedia.org", "course": self.course.id}
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_retrieve(self):
        """Тест получения деталей урока владельцем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-get', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.lesson.title)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-update', kwargs={'pk': self.lesson.pk})
        data = {"title": "Updated DRF Intro"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_permissions(self):
        """Тест ограничений модератора (нельзя создавать и удалять)"""
        self.client.force_authenticate(user=self.moderator)

        # Попытка создания
        create_url = reverse('materials:lesson-create')
        data = {"title": "Moder Lesson", "video_url": "https://youtube.com", "course": self.course.id}
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Попытка удаления
        delete_url = reverse('materials:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription_toggle(self):
        """Тест работы механизма подписки"""
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:course-subscribe')
        data = {"course_id": self.course.id}

        # Первое переключение — добавление
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Второе переключение — удаление
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
