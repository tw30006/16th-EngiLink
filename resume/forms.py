from django import forms
from .models import Profile
from datetime import date

class ProfileForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(choices=Profile.SKILL_CHOICES, widget=forms.CheckboxSelectMultiple)
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1960, 2025)),
        initial=date(1990, 1, 15), 
        required=False
    )
    class Meta:
        model = Profile
        exclude = ['deleted_at','created_at']
    
    def clean_skills(self):
        return ', '.join(self.cleaned_data['skills'])