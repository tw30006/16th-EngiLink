from django.db import models
from django.utils import timezone


class JobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class Job(models.Model):
    title = models.CharField(max_length=100)
    openings = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    description = models.TextField(default="")
    deleted_at = models.DateTimeField(null=True)

    objects = JobManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
