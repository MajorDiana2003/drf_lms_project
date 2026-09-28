from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from users.apps import UsersConfig
from users.views import UserProfileAPIView, PaymentListAPIView, UserCreateAPIView
from users.views import PaymentCreateAPIView, PaymentStatusAPIView


app_name = UsersConfig.name

urlpatterns = [

    path("profile/<int:pk>/", UserProfileAPIView.as_view(), name="user-profile"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/status/<int:pk>/', PaymentStatusAPIView.as_view(), name='payment-status'),
]
