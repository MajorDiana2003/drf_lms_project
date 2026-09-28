from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsModer, IsOwner


# Контроллер для Курсов
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    # Динамически фильтруем список курсов для обычных пользователей
    def get_queryset(self):
        if self.request.user.groups.filter(name="модераторы").exists():
            return Course.objects.all()
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

    # Дополнительно: чтобы обычные юзеры не видели чужие уроки в списке
    def get_queryset(self):
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
