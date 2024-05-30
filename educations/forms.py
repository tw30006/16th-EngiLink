from django import forms
from .models import Education
from datetime import date

class EducationForm(forms.ModelForm):
    default_date = date(1990, 1, 15)
    date_widget = forms.SelectDateWidget(years=range(1960, 2025))
    start_date = forms.DateTimeField(input_formats=["%Y-%m"], widget=forms.DateInput(attrs={'type': 'month'}), required=False)
    end_date = forms.DateTimeField(input_formats=["%Y-%m"], widget=forms.DateInput(attrs={'type': 'month'}), required=False)
    field_labels = {
        "school_name": "校名",
        "major": "專業",
        "degree": "學位",
        "start_date": "入學時間",
        "end_date": "畢業時間",
    }

    class Meta:
        model = Education
        exclude = ["deleted_at", "created_at", "posit"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field_name, label in self.field_labels.items():
            self.fields[field_name].label = label
