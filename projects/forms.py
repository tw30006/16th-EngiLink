from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    technologies_used= forms.MultipleChoiceField(choices=Project.SKILL_CHOICES, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Project
        exclude = ['deleted_at','created_at']
        
    def clean_skills(self):
        return ', '.join(self.cleaned_data['technologies_used'])