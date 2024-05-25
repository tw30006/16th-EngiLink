from django.db import models
from django.utils import timezone
from resumes.models import Resume
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from companies.models import Company
import re
from users.models import CustomUser


class JobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


OPENINGS_CHOICES = [(i, str(i)) for i in range(1, 11)]


def validate_letters_and_chinese(value):
    if not re.match(r"^[a-zA-Z\u4e00-\u9fa5]+$", value):
        raise ValidationError("欄位只能填寫中文或英文")


def validate_taiwan_address(value):
    address_re = r"^(台北市|新北市|桃園市|台中市|台南市|高雄市|基隆市|新竹市|新竹縣|苗栗縣|彰化縣|南投縣|雲林縣|嘉義市|嘉義縣|屏東縣|宜蘭縣|花蓮縣|台東縣|澎湖縣|金門縣|連江縣)[\u4e00-\u9fa5]+(?:區|市|鎮|鄉)?[\u4e00-\u9fa5]*(?:路|街|巷)[\u4e00-\u9fa5]*[0-9]*號(?:之[0-9]+)?(?:[-0-9樓]+)?$"
    if not re.match(address_re, value):
        raise ValidationError("請輸入正確的地址")


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
    experience = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(50, message="年資必須低於50"),
        ]
    )
    salary = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(0)])
    address = models.CharField(max_length=250, validators=[validate_taiwan_address])
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
    status = models.CharField(max_length=20, default='applied') 
    withdrawn_at = models.DateTimeField(null=True, blank=True) 


class User_Job(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    collect = models.BooleanField(default=False)
