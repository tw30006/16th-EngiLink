from django.urls import path
from .views import EducationUpdateView, EducationDeleteView

app_name = "educations"

urlpatterns = [
    path("<pk>/edit", EducationUpdateView.as_view(), name="edu_edit"),
    path("<pk>/delete", EducationDeleteView.as_view(), name="edu_delete"),
]
