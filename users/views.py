
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserPublicSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, retrieve_stripe_session


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Проверяем, идет ли сканирование документации
        if getattr(self, 'swagger_tester', None) or self.kwargs.get('pk') is None:
            return UserSerializer

        try:
            # Безопасно проверяем, совпадает ли запрашиваемый объект с текущим пользователем
            if self.get_object() == self.request.user:
                return UserSerializer
        except Exception:
            pass

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


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product_name = payment.paid_course.title if payment.paid_course else payment.paid_lesson.title

        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(payment.amount, product_id)
        session_id, payment_link = create_stripe_session(price_id)

        payment.stripe_product_id = product_id
        payment.stripe_price_id = price_id
        payment.stripe_session_id = session_id
        payment.payment_link = payment_link
        payment.save()


class PaymentStatusAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()

        if payment.stripe_session_id:
            status = retrieve_stripe_session(payment.stripe_session_id)
            if status == "paid":
                payment.payment_method = "transfer"
                payment.save()
            return Response({"stripe_status": status, "payment_id": payment.id})

        return Response({"error": "Сессия Stripe не найдена"}, status=400)
