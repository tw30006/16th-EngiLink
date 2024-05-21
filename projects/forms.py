from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    technologies_used = forms.MultipleChoiceField(
        choices=Project.SKILL_CHOICES, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        exclude = ["deleted_at", "created_at", "posit"]

    field_labels = {
        "project_name": "專案名稱",
        "responsibility": "負責項目",
        "technologies_used": "技能使用",
        "description": "說明",
    }

    def clean_skills(self):
        return ", ".join(self.cleaned_data["technologies_used"])

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field_name, label in self.field_labels.items():
            self.fields[field_name].label = label
