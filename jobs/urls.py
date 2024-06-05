from django.urls import path
from .views import (
    ShowView,
    EditView,
    JobDeleteView,
    PublishView,
    JobListView,
    JobDetailView,
)


app_name = "jobs"

urlpatterns = [
    path("list/", JobListView.as_view(), name="job_list"),
    path("detail/<pk>/", JobDetailView.as_view(), name="job_detail"),
    path("edit/<pk>/", EditView.as_view(), name="edit"),
    path("delete/<pk>/", JobDeleteView.as_view(), name="delete"),
    path("publish/<pk>", PublishView.as_view(), name="publish"),
    path("<pk>/", ShowView.as_view(), name="show"),
]
