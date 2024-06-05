from django.db import models
from django.utils import timezone
from positions.fields import PositionField
from resumes.models import Resume


class Work(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="works")
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(
        choices=[(True, "是"), (False, "否")], default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    posit = PositionField(collection="resume")
    objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
