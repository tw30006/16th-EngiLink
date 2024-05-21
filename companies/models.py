from django.db import models
from users.models import CustomUser


class Company(models.Model):
    company_name = models.CharField(max_length=100,default='')
    tin = models.CharField(max_length=8,default='')
    user_name = models.CharField(max_length=100,default='')
    tel = models.CharField(max_length=11,default='')
    custom_user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    description = models.TextField(default='')
    area = models.CharField(max_length=50, default='')
    type = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name
