"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("resumes/", include("resumes.urls")),
    path("dashboard/", include("users.urls")),
    path("jobs/", include("jobs.urls")),
    path("companies/", include("companies.urls")),
    path("accounts/", include("allauth.urls")),
    path("educations/", include("educations.urls")),
    path("works/", include("works.urls")),
    path("projects/", include("projects.urls")),
    path("api/v1/resumes/",include("resumes.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
