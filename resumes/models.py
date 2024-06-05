from django.db import models
from django.utils import timezone
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

User = settings.AUTH_USER_MODEL


class ResumeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class Resume(models.Model):
    GENDER_CHOICES = [
        ("M", "男"),
        ("F", "女"),
        ("N", "不透露"),
    ]
    EXPERIENCE_CHOICES = [
        ("1年以下", "一年以下"),
        ("3年以下", "三年以下"),
        ("3年以上", "三年以上"),
        ("5年以上", "五年以上"),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    experience = models.CharField(
        max_length=20, choices=EXPERIENCE_CHOICES, null=True, blank=True
    )
    skills = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    picture = models.FileField(null=True)
    posit = models.IntegerField(default=0)
    style = models.IntegerField(default=1)

    objects = ResumeManager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def get_skills(self):
        return self.skills

    def save(self, *args, **kwargs):
        if self.picture:
            img = Image.open(self.picture)
            max_size = (300, 300)
            img.thumbnail(max_size, Image.LANCZOS)
            thumb_io = BytesIO()
            img_format = "PNG" if img.mode == "RGBA" else "JPEG"
            img.save(thumb_io, format=img_format)
            thumb_io.seek(0)
            file_extension = "png" if img.mode == "RGBA" else "jpg"
            new_file_name = f"{self.picture.name.split('.')[0]}_thumb.{file_extension}" 
            self.picture.save(new_file_name, ContentFile(thumb_io.read()), save=False)
        super().save(*args, **kwargs)
