from django.urls import path
from .views import ProjectUpdateView, ProjectDeleteView

app_name = "projects"

urlpatterns = [
    path("<pk>/edit", ProjectUpdateView.as_view(), name="project_edit"),
    path("<pk>/delete", ProjectDeleteView.as_view(), name="project_delete"),
]


