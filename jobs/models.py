from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from companies.models import Company
from resumes.models import Resume
from users.models import CustomUser


class JobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


OPENINGS_CHOICES = [(i, str(i)) for i in range(1, 11)]


def validate_taiwan_address(value):
    pass


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=100)
    openings = models.IntegerField(
        choices=OPENINGS_CHOICES,
        default=1,
        verbose_name="openings",
    )
    resumes = models.ManyToManyField(Resume, through="Job_Resume")
    users = models.ManyToManyField(CustomUser, through="User_Job")
    experience = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    salary = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(0)])
    address = models.CharField(max_length=250, default="")
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    is_published = models.BooleanField(default=False)

    objects = JobManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()


class Job_Resume(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="applied")
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_invitation = models.TextField(null=True, blank=True)
    accepted = models.CharField(max_length=20, default=None, null=True)


class User_Job(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    collect = models.BooleanField(default=False)
