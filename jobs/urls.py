from django.urls import path
from .views import ShowView, EditView, JobDeleteView,SetPublishView

app_name = "jobs"

urlpatterns = [
    path("edit/<pk>/", EditView.as_view(), name="edit"),
    path("delete/<pk>/", JobDeleteView.as_view(), name="delete"),
    path("setpublish/<pk>", SetPublishView.as_view(), name="setpublish"),
    path("<pk>/", ShowView.as_view(), name="show"),
]
