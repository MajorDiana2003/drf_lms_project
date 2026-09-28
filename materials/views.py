from rest_framework import viewsets, generics
from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsModer, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from materials.paginators import MaterialsPagination


# Контроллер для Курсов
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    # Динамически фильтруем список курсов для обычных пользователей
    def get_queryset(self):
        # Если пользователь не авторизован
        if not self.request.user.is_authenticated:
            return Course.objects.none()

        # Если это модератор
        if self.request.user.groups.filter(name="модераторы").exists():
            return Course.objects.all()

        # Для обычных владельцев
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Разделение прав по действиям (actions)
    def get_permissions(self):
        if self.action == 'create':
            # Создавать модераторам нельзя
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Просматривать и редактировать могут и модераторы, и владельцы
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == 'destroy':
            # Удалять модераторам нельзя, только владелец
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            # Для остальных действий (например, list)
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


# Контроллеры для Уроков (Generic-классы)
# 1. Создание урока: доступно всем авторизованным, кроме модераторов
class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 2. Список уроков: видят владельцы (свои) и модераторы (все)
class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]
    pagination_class = MaterialsPagination

    # Дополнительно: чтобы обычные юзеры не видели чужие уроки в списке
    def get_queryset(self):
        # Безопасное отсечение неавторизованных запросов от Swagger
        if not self.request.user.is_authenticated:
            return Lesson.objects.none()

        if self.request.user.groups.filter(name="модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


# 3. Просмотр одного урока: доступно модераторам или владельцу
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


# 4. Редактирование урока: доступно модераторам или владельцу
class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


# 5. Удаление урока: доступно ТОЛЬКО владельцу (модераторам нельзя)
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        # Получаем объект курса из базы данных
        course_item = get_object_or_404(Course, id=course_id)

        # Ищем подписку текущего пользователя на этот курс
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть — удаляем
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки нет — создаем
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})
