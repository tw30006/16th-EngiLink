from django.contrib import admin
from .models import Resume
from .forms import ResumeForm


class ResumeAdmin(admin.ModelAdmin):
    form = ResumeForm
    exclude = ["deleted_at", "created_at"]
    radio_fields = {"gender": admin.HORIZONTAL, "experience": admin.HORIZONTAL}


admin.site.register(Resume, ResumeAdmin)
