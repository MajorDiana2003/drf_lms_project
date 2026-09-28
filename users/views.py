
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserPublicSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Если пользователь запрашивает свой профиль, отдаем полный сериализатор
        if self.get_object() == self.request.user:
            return UserSerializer
        # Если чужой — отдаем урезанный сериализатор с общей информацией
        return UserPublicSerializer

    def get_permissions(self):
        # Редактировать (PUT/PATCH) профиль может только его владелец
        if self.request.method in ['PUT', 'PATCH']:
            from materials.permissions import IsOwner
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            # Просматривать (GET) может любой авторизованный пользователь
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Настройки фильтрации
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

    # Настройки сортировки
    ordering_fields = ('payment_date',)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
