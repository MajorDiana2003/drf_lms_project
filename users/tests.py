from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course
from users.models import User, Payment


class PaymentTestCase(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(email="test@example.com")
        self.user.set_password("password123")
        self.user.save()

        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые курсы
        self.course_django = Course.objects.create(title="Django")
        self.course_python = Course.objects.create(title="Python")

        # Создаем тестовые платежи для проверки фильтрации и сортировки
        self.payment_1 = Payment.objects.create(
            user=self.user,
            paid_course=self.course_django,
            amount=1000.00,
            payment_method="cash",
            payment_date="2026-01-01T12:00:00Z"
        )
        self.payment_2 = Payment.objects.create(
            user=self.user,
            paid_course=self.course_python,
            amount=2000.00,
            payment_method="transfer",
            payment_date="2026-01-02T12:00:00Z"
        )

        self.url = reverse('users:payment-list')

    def test_payment_filter_by_course(self):
        """Тест фильтрации платежей по курсу"""
        response = self.client.get(self.url, {'paid_course': self.course_django.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что вернулся только 1 платеж, принадлежащий курсу Django
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['paid_course'], self.course_django.id)

    def test_payment_sorting_by_date_ascending(self):
        """Тест сортировки платежей по дате по возрастанию"""
        response = self.client.get(self.url, {'ordering': 'payment_date'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем правильный порядок (сначала payment_1 от 01 января, затем payment_2 от 02 января)
        self.assertEqual(response.json()[0]['id'], self.payment_1.id)
        self.assertEqual(response.json()[1]['id'], self.payment_2.id)

    def test_payment_sorting_by_date_descending(self):
        """Тест сортировки платежей по дате по убыванию"""
        response = self.client.get(self.url, {'ordering': '-payment_date'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем обратный порядок (сначала payment_2, затем payment_1)
        self.assertEqual(response.json()[0]['id'], self.payment_2.id)
        self.assertEqual(response.json()[1]['id'], self.payment_1.id)
