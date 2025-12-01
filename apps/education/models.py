from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator
from decimal import Decimal


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class BaseSoftDelete(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()         
    all_objects = SoftDeleteQuerySet.as_manager()  

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete: just add deleted_at."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """Complete removal from the database (if necessary)."""
        return super().delete(using=using, keep_parents=keep_parents)


class Course(BaseSoftDelete):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_courses",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Lesson(BaseSoftDelete):
    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    order = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    indentation = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(5)],
    )

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course_id}: {self.title}"
