
from django.urls import path
from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Маршрут для редактирования и просмотра профиля
    path('profile/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-profile'),
]
