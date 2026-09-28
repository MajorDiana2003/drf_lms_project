from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле Email обязательно для заполнения")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватарка",
        blank=True,
        null=True,
        help_text="Загрузите аватарку",
    )

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата оплаты',
    )
    paid_course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments',
        verbose_name='Оплаченный курс'
    )
    paid_lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments',
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(
        max_length=10,
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='transfer',
        verbose_name='Способ оплаты'
    )
    stripe_product_id = models.CharField(
        max_length=255, verbose_name="ID продукта Stripe", blank=True, null=True
    )
    stripe_price_id = models.CharField(
        max_length=255, verbose_name="ID цены Stripe", blank=True, null=True
    )
    stripe_session_id = models.CharField(
        max_length=255, verbose_name="ID сессии Stripe", blank=True, null=True
    )
    payment_link = models.TextField(
        verbose_name="Ссылка на оплату", blank=True, null=True
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.user.email} - {self.amount} ({self.get_payment_method_display()})'
