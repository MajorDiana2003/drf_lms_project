from django.urls import path
from users.apps import UsersConfig
from users.views import UserProfileAPIView, PaymentListAPIView


app_name = UsersConfig.name

urlpatterns = [
    # Обновили контроллер на просмотр профиля
    path("profile/<int:pk>/", UserProfileAPIView.as_view(), name="user-profile"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]
