from django.urls import path
from .views import SignupView, UserIndexView, ProfileUpdateView, UserProfileView, SigninView, SignoutView
from django.contrib.auth import views as auth_views
from resumes.views import ResumeArea

app_name = "users"

urlpatterns = [
    path("", UserIndexView.as_view(), name="userindex"),
    path("resume/", ResumeArea.as_view(), name="resume"),
    path("signup/", SignupView.as_view(), name="users_signup"),
    path("edit/", ProfileUpdateView.as_view(template_name="users/edit.html"), name="users_edit"),
    path("signin/", SigninView.as_view(), name="users_signin"),
    path("signout/", SignoutView.as_view(), name="users_signout"),
    path("show/<int:pk>/", UserProfileView.as_view(), name="users_profile"),
]