from django.db import models
from resumes.models import Resume
from positions.fields import PositionField
import ast

class Project(models.Model):
    SKILL_CHOICES = [
        (skill, skill)
        for skill in [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "HTML/CSS",
            "PHP",
            "Ruby",
            "Swift",
            "其他",
        ]
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,related_name='projects')
    project_name = models.CharField(max_length=100)
    responsibility = models.CharField(max_length=200)
    technologies_used = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    posit = PositionField(collection='resume')

    objects = models.Manager()

    def get_technologies(self):
        try:
            return ast.literal_eval(self.technologies_used)
        except:
            return []
