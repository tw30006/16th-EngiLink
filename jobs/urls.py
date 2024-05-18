from django.urls import path
from .views import ShowView, EditView, JobDeleteView,SetPublishView

app_name = "jobs"

urlpatterns = [
    path("edit/<int:pk>/", EditView.as_view(), name="edit"),
    path("delete/<int:pk>/", JobDeleteView.as_view(), name="delete"),
    path("setpublish/<int:pk>", SetPublishView.as_view(), name="setpublish"),
    path("<int:pk>/", ShowView.as_view(), name="show"),
]
