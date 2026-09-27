from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)


    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        )

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с текущим курсом"""
        return obj.lessons.count()

