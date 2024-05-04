from django.urls import path
from .views import IndexView, AddView, ShowView, EditView, JobDeleteView

app_name = "jobs"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create", AddView.as_view(), name="create"),
    path("edit/<pk>", EditView.as_view(), name="edit"),
    path("delete/<pk>", JobDeleteView.as_view(), name="delete"),
    path("<pk>", ShowView.as_view(), name="show"),
]
