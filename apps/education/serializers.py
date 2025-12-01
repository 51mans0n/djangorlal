from rest_framework import serializers
from apps.education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "owner",
            "lessons_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "owner", "lessons_count"]

    def create(self, validated_data):
        request = self.context["request"]
        return Course.objects.create(owner=request.user, **validated_data)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "content",
            "order",
            "indentation",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "course",
            "order",
            "indentation",
            "created_at",
            "updated_at",
        ]
