from django.db import models
from resume.models import Profile
from django.utils import timezone

class EducationsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class Educations(models.Model):
    DEGREE_CHOICES = [
        ('1', '高中職以下'),
        ('2', '高中職'),
        ('3', '專科'),
        ('4', '學士'),
        ('5', '碩士'),
        ('6', '博士'),
        ('7', '肄業'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    degree = models.CharField(max_length=1, choices=DEGREE_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    edu_objects = EducationsManager()  

    def __str__(self):
        return f"{self.name}'s Profile ({self.profile_id})"

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()  
        self.save()
        super(Educations, self).delete(*args, **kwargs)
