from django.forms import ModelForm
from .models import Job


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ["title", "openings", "experience", "salary", "address", "description","is_published"]
        labels = {
            "title": "職位名稱",
            "openings": "人數需求",
            "experience": "工作經驗",
            "salary": "工作薪資",
            "address": "工作地點",
            "description": "工作內容",
            "is_published":"是否刊登"
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
