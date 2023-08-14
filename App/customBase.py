from django.db import models
from django.db.models.query import QuerySet


class CustomQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        return super(self.__class__, self).__init__(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for obj in self: obj.delete()


class CustomManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return CustomQuerySet(model=self.model, using=self._db, hints=self._hints).filter(is_deleted=False)

    def all_with_deleted(self, *args, **kwargs):
        return CustomQuerySet(model=self.model, using=self._db, hints=self._hints).filter()

    def deleted_set(self, *args, **kwargs):
        return CustomQuerySet(model=self.model, using=self._db, hints=self._hints).filter(is_deleted=True)

    def get(self, *args, **kwargs):
        """ if a specific record was requested, return it even if it's deleted """
        return self.all_with_deleted().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        """ if pk was specified as a kwarg, return even if it's deleted """
        if 'pk' in kwargs:
            return self.all_with_deleted().filter(*args, **kwargs)
        return self.get_queryset().filter(*args, **kwargs)


class CustomModel(models.Model):
    objects = CustomManager()
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")

    def delete(self, *args, **kwargs):
        if self.is_deleted:
            return
        self.is_deleted = True
        self.save()

    def erase(self, *args, **kwargs):
        """
        Actually delete from database.
        """
        super(CustomModel, self).delete(*args, **kwargs)

    def restore(self, *args, **kwargs):
        if not self.is_deleted:
            return
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True
