from django.db import models
from users.models import CustomUser


class Company(models.Model):
    company_name = models.CharField(max_length=100, default="")
    tin = models.CharField(max_length=8, default="")
    user_name = models.CharField(max_length=100, default="")
    tel = models.CharField(max_length=11, default="")
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250, default="")
    description = models.TextField(default="")
    type = models.CharField(max_length=50, default="")
    banner = models.ImageField(upload_to="banners/", null=True, blank=True)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

class User_Company(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    collect = models.BooleanField(default=False)
