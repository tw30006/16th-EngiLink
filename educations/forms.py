from django import forms
from .models import Education
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class EducationForm(forms.ModelForm):
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
        "school_name": "校名",
        "major": "專業",
        "degree": "學位",
        "start_date": "入學時間",
        "end_date": "畢業時間",
    }

    class Meta:
        model = Education
        exclude = ["resume", "deleted_at", "created_at", "posit"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field_name, label in self.field_labels.items():
            self.fields[field_name].label = label

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise ValidationError(_("入學時間不能晚於畢業時間"))

        return cleaned_data