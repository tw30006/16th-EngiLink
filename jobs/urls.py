from django.urls import path
from . import views
from .views import IndexView, AddView

app_name = "jobs"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create", AddView.as_view(), name="create"),
]
