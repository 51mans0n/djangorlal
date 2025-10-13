from django.db import models
from django.utils import timezone

class SoftDeleteQuerySet(models.QuerySet):
    """QS с удобными методами для soft/hard delete."""
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """Менеджер, скрывающий помеченные на удаление записи."""
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    # полезно иметь быстрый доступ к «всем»
    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).all()


class AbstractSoftDeletableModel(models.Model):
    """
    Базовая абстрактная модель с полями soft-delete и переопределённым delete().
    Наследуем ЕЁ вместо models.Model во всех ваших моделях (catalogs/commerces).
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Менеджеры:
    objects = SoftDeleteManager()            # «живые» записи (is_deleted=False)
    all_objects = SoftDeleteQuerySet.as_manager()  # все, + методы alive()/dead()/hard_delete()

    class Meta:
        abstract = True

    # мягкое удаление конкретного объекта
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    # жёсткое удаление конкретного объекта (осторожно!)
    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    # восстановление
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])
