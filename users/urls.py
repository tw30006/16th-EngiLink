from django.urls import path
from .views import SignupView, UserIndexView, ProfileUpdateView, UserProfileView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", UserIndexView.as_view(), name="userindex"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("edit/", ProfileUpdateView.as_view(template_name="users/edit.html"), name="edit"),
    path("signin/", auth_views.LoginView.as_view(template_name="users/signin.html"), name="signin"),
    path("signout/", auth_views.LogoutView.as_view(template_name="users/signout.html"), name="signout"),
    path("show/<int:pk>/", UserProfileView.as_view(), name="profile"),
]