from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.education.models import Course, Lesson


class IsCourseOwner(BasePermission):
    """
    Allows access only to the course owner.
    For Lesson, use course.owner.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return obj.owner == request.user
        if isinstance(obj, Lesson):
            return obj.course.owner == request.user
        return False
