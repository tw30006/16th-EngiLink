from django.urls import path
from .views import WorkUpdateView, WorkDeleteView

app_name = "works"

urlpatterns = [
    path("<pk>/edit", WorkUpdateView.as_view(), name="work_edit"),
    path("<pk>/delete", WorkDeleteView.as_view(), name="work_delete"),
]

