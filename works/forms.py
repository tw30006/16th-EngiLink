from django import forms
from .models import Work


class WorkForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        input_formats=["%Y-%m"],
        widget=forms.DateInput(attrs={"type": "month"}),
        required=False,
    )
    end_date = forms.DateTimeField(
        input_formats=["%Y-%m"],
        widget=forms.DateInput(attrs={"type": "month"}),
        required=False,
    )
    field_labels = {
        "company_name": "公司名",
        "position": "職位",
        "start_date": "入職時間",
        "end_date": "離職時間",
        "is_current": "在職中",
    }

    class Meta:
        model = Work
        exclude = ["resume", "deleted_at", "created_at", "posit"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field_name, label in self.field_labels.items():
            self.fields[field_name].label = label
