from decimal import Decimal

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.education.models import Course, Lesson
from apps.education.serializers import CourseSerializer, LessonSerializer
from apps.education.permissions import IsCourseOwner

class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Course.objects.annotate(
            lessons_count=Count("lessons", filter=Q(lessons__deleted_at__isnull=True))
        )

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            val = is_active.lower()
            if val == "true":
                qs = qs.filter(is_active=True)
            elif val == "false":
                qs = qs.filter(is_active=False)

        return qs


    def list(self, request):
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CourseSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(CourseSerializer(course, context={"request": request}).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        course = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = CourseSerializer(course, context={"request": request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        self.check_object_permissions(request, course)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(course, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        course.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="activate", permission_classes=[IsAuthenticated, IsCourseOwner])
    def activate(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if course.is_active:
            return Response({"detail": "Course already active."}, status=status.HTTP_400_BAD_REQUEST)
        course.is_active = True
        course.save(update_fields=["is_active"])
        return Response(CourseSerializer(course, context={"request": request}).data)

    @action(detail=True, methods=["post"], url_path="deactivate", permission_classes=[IsAuthenticated, IsCourseOwner])
    def deactivate(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if not course.is_active:
            return Response({"detail": "Course already inactive."}, status=status.HTTP_400_BAD_REQUEST)
        course.is_active = False
        course.save(update_fields=["is_active"])
        return Response(CourseSerializer(course, context={"request": request}).data)

    @action(detail=True, methods=["get"], url_path="lessons", permission_classes=[IsAuthenticated, IsCourseOwner])
    def lessons(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        self.check_object_permissions(request, course)
        lessons = course.lessons.all()  
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.select_related("course", "course__owner")

    def create(self, request):
        """
        Body: { "course_id": ..., "title": "...", "content": "..." }
        We take and set the course_id ourselves (we don't allow 
        you to specify the course directly),
        We set the order to "top" (minimum - 1).
        """
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"detail": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course.objects.all(), pk=course_id)
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        title = request.data.get("title", "")
        content = request.data.get("content", "")

        existing = Lesson.all_objects.filter(course=course).order_by("order").first()
        if existing:
            new_order = existing.order - Decimal("1.00")
        else:
            new_order = Decimal("0.00")

        lesson = Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            order=new_order,
            indentation=0,
        )
        serializer = LessonSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["put"], url_path="move", permission_classes=[IsAuthenticated])
    def move(self, request, pk=None):
        """
        Body: { "before_lesson_id": <id or null> }
        """
        lesson = get_object_or_404(self.get_queryset(), pk=pk)
        if lesson.course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        before_id = request.data.get("before_lesson_id")
        qs_same_course = Lesson.all_objects.filter(course=lesson.course)

        if before_id:
            before = get_object_or_404(qs_same_course, pk=before_id)
            new_order = before.order - Decimal("0.01")
            lesson.indentation = min(before.indentation, 5)
        else:
            last = qs_same_course.order_by("-order").first()
            if last:
                new_order = last.order + Decimal("1.00")
            else:
                new_order = Decimal("0.00")
            lesson.indentation = 0

        lesson.order = new_order
        lesson.save(update_fields=["order", "indentation"])
        return Response({"id": lesson.id, "order": str(lesson.order), "indentation": lesson.indentation})

    def destroy(self, request, pk=None):
        lesson = get_object_or_404(self.get_queryset(), pk=pk)
        if lesson.course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        lesson.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="publish", permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        lesson = get_object_or_404(self.get_queryset(), pk=pk)
        if lesson.course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        lesson.is_published = True
        lesson.save(update_fields=["is_published"])
        return Response(LessonSerializer(lesson).data)

    @action(detail=True, methods=["post"], url_path="unpublish", permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        lesson = get_object_or_404(self.get_queryset(), pk=pk)
        if lesson.course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        lesson.is_published = False
        lesson.save(update_fields=["is_published"])
        return Response(LessonSerializer(lesson).data)
