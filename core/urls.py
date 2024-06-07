from django.contrib import admin
from django.urls import path, include
from .views import CustomTemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include
import os

urlpatterns = [
    path(os.getenv("ADMIN_URL"), admin.site.urls),
    path("", CustomTemplateView.as_view(), name="home"),
    path("resumes/", include("resumes.urls")),
    path("users/", include("users.urls")),
    path("jobs/", include("jobs.urls")),
    path("companies/", include("companies.urls")),
    path("accounts/", include("allauth.urls")),
    path("educations/", include("educations.urls")),
    path("works/", include("works.urls")),
    path("projects/", include("projects.urls")),
    path("api/v1/resumes/",include("resumes.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
