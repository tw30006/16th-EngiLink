from django.db import models
from django.utils import timezone


class JobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


OPENINGS_CHOICES = [(i, str(i)) for i in range(1, 11)]


class Job(models.Model):
    title = models.CharField(max_length=100)
    openings = models.IntegerField(
        choices=OPENINGS_CHOICES,
        default=1,
        verbose_name="openings",
    )
    experience = models.CharField(max_length=100)
    salary = models.IntegerField(blank=True)
    address = models.CharField(max_length=250)
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = JobManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
