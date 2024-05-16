from django.urls import path
from .views import (
    ResumeArea,
    ResumeListView,
    ResumeCreateView,
    ResumeUpdateView,
    ResumeDeleteView,
    TotalListView,
    GenerateResumePdf,
)
from educations.views import (
    EducationCreateView,
    EducationListView,
    EducationUpdateView,
    EducationDeleteView,
)
from works.views import (
    WorkCreateView,
    WorkListView,
    WorkUpdateView,
    WorkDeleteView,
)
from projects.views import (
    ProjectCreateView,
    ProjectListView,
    ProjectUpdateView,
    ProjectDeleteView,
)


app_name = "resumes"

urlpatterns = [
    path("", ResumeArea.as_view(), name="index"),
    path("create/", ResumeCreateView.as_view(), name="create"),
    path("edit/<pk>", ResumeUpdateView.as_view(), name="edit"),
    path("delete/<pk>", ResumeDeleteView.as_view(), name="delete"),
    path("resume/<int:resume_id>/pdf/", GenerateResumePdf, name="generate_resume_pdf"),
    path("total/<int:resume_id>", TotalListView.as_view(), name="total"),


    path("edu/", EducationCreateView.as_view(), name="edu"),
    path("edu/show/", EducationListView.as_view(), name="edu-show"),
    path("edu/edit/<pk>", EducationUpdateView.as_view(), name="edu-edit"),
    path("edu/delete/<pk>", EducationDeleteView.as_view(), name="edu-delete"),


    path("work/", WorkCreateView.as_view(), name="work"),
    path("work/show/", WorkListView.as_view(), name="work-show"),
    path("work/edit/<pk>", WorkUpdateView.as_view(), name="work-edit"),
    path("work/delete/<pk>", WorkDeleteView.as_view(), name="work-delete"),


    path("project/", ProjectCreateView.as_view(), name="project"),
    path("project/show/", ProjectListView.as_view(), name="project-show"),
    path("project/edit/<pk>", ProjectUpdateView.as_view(), name="project-edit"),
    path("project/delete/<pk>", ProjectDeleteView.as_view(), name="project-delete"),


    path("<pk>/", ResumeListView.as_view(), name="show"),
]
