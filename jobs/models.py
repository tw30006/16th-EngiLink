from django.db import models


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)
    openings = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    description = models.TextField(default="")
