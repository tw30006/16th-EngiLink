from django.urls import path
from .views import (
    ResumeArea,
    ResumeListView,
    ResumeCreateView,
    ResumeUpdateView,
    ResumeDeleteView,
    TotalListView,
    generate_pdf_1,
    generate_pdf_2,
    generate_pdf_3,
    update_positions,
    UpdateStyleView,
    update_template,
)
from educations.views import EducationCreateView, EducationListView
from works.views import WorkCreateView, WorkListView
from projects.views import ProjectCreateView, ProjectListView

app_name = "resumes"

urlpatterns = [
    path("", ResumeArea.as_view(), name="index"),
    path("create/", ResumeCreateView.as_view(), name="create"),
    path("edit/<pk>", ResumeUpdateView.as_view(), name="edit"),
    path("delete/<pk>", ResumeDeleteView.as_view(), name="delete"),
    path("resume/<int:resume_id>/pdf_1/", generate_pdf_1, name="generate_pdf_1"),
    path("resume/<int:resume_id>/pdf_2/", generate_pdf_2, name="generate_pdf_2"),
    path("resume/<int:resume_id>/pdf_3/", generate_pdf_3, name="generate_pdf_3"),
    path("total/<int:resume_id>", TotalListView.as_view(), name="total"),
    path("update_positions/", update_positions, name="update_positions"),
    path("<pk>/education/", EducationCreateView.as_view(), name="education"),
    path("<pk>/educations/", EducationListView.as_view(), name="educations"),
    path("<pk>/work/", WorkCreateView.as_view(), name="work"),
    path("<pk>/works/", WorkListView.as_view(), name="works"),
    path("<pk>/project/", ProjectCreateView.as_view(), name="project"),
    path("<pk>/projects/", ProjectListView.as_view(), name="projects"),
    path("update_style/<int:resume_id>", UpdateStyleView.as_view(), name="update_style"),
    path("<int:resume_id>/update_template", update_template, name="update_template"),
    path("<pk>/", ResumeListView.as_view(), name="show"),
]
