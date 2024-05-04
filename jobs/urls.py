from django.urls import path
from . import views
from .views import IndexView, AddView, ShowView, EditView

app_name = "jobs"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create", AddView.as_view(), name="create"),
    path("edit/<pk>", EditView.as_view(), name="edit"),
    path("<pk>", ShowView.as_view(), name="show"),
]
