from django.urls import path
from .views import ShowView, EditView, JobDeleteView

app_name = "jobs"

urlpatterns = [
    path("edit/<pk>/", EditView.as_view(), name="edit"),
    path("delete/<pk>/", JobDeleteView.as_view(), name="delete"),
    path("<pk>/", ShowView.as_view(), name="show"),
]
