from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Поля, которые можно просматривать и редактировать
        fields = ('id', 'email', 'phone', 'city', 'avatar', 'password')
        # Скрываем пароль при выводе информации из соображений безопасности
        extra_kwargs = {'password': {'write_only': True}}
