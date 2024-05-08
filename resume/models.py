from django.db import models
from django.utils import timezone
from django.conf import settings
User = settings.AUTH_USER_MODEL


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('N', '不透露'),
    ]
    EXPERIENCE_CHOICES = [
        ('1年以下', '一年以下'),
        ('3年以下', '三年以下'),
        ('3年以上', '三年以上'),
        ('5年以上', '五年以上'),
    ]
    SKILL_CHOICES = [(skill, skill) for skill in ['Python', 'JavaScript', 'Java', 'C++', 'HTML/CSS', 'PHP', 'Ruby', 'Swift', '其他']]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, null=True, blank=True)
    skills = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    

    objects =ProfileManager() 

    def __str__(self):
        return f"{self.name}'s Profile ({self.profile_id})"

    def delete(self):
        self.deleted_at = timezone.now()  
        self.save()
    
    def get_skills(self):
        return self.skills.split(', ')


    
class EducationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class Education(models.Model):
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
    edu_objects = EducationManager()  

    def __str__(self):
        return f"{self.name}'s Profile ({self.profile_id})"

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()  
        self.save()
        super(Education, self).delete(*args, **kwargs)


class Work(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()  
    def __str__(self):
        return f"{self.name}'s Profile ({self.profile_id})"

    def soft_delete(self):
        self.deleted_at = timezone.now() 
        self.save()


class Project(models.Model):
    SKILL_CHOICES = [(skill, skill) for skill in ['Python', 'JavaScript', 'Java', 'C++', 'HTML/CSS', 'PHP', 'Ruby', 'Swift', '其他']]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    responsibility = models.CharField(max_length=200)
    technologies_used = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null = True)


    objects = models.Manager() 

    def __str__(self):
        return f"{self.name}'s Profile ({self.profile_id})"
    
    def get_technologies(self):
        return self.technologies_used.split(', ')
