from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re

class Company(AbstractUser):
    email = models.EmailField(max_length=255)
    company_name = models.CharField(max_length=100)
    tin = models.CharField(max_length=8)
    user_name = models.CharField(max_length=100)
    tel = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def clean(self):
        if Company.objects.filter(email=self.email).exclude(id=self.id).exists():
            raise ValidationError("這個電子郵件已經被註冊")
        if not re.match(r'^[\u4e00-\u9fa5]{5,}$', self.company_name):
            raise ValidationError("公司名稱格式不正確")
        if not re.match(r'^\d{8}$', self.tin):
            raise ValidationError("統一編號應為 8 位數字")
        if not re.match(r'^[\u4e00-\u9fa5]{2,}$', self.user_name):
            raise ValidationError("姓名格式不正確")
        if not re.match(r'^(0\d{1,2}-?\d{6,8})$', self.tel):
            raise ValidationError("電話號碼格式不正確")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
