from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payment
from users.serializers import PaymentSerializer

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Настройки фильтрации
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

    # Настройки сортировки
    ordering_fields = ('payment_date',)