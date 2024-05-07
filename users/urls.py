from django.urls import path
from .views import SignupView, UserIndexView, ProfileUpdateView, UserProfileView, SigninView, SignoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", UserIndexView.as_view(), name="userindex"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("edit/", ProfileUpdateView.as_view(template_name="users/edit.html"), name="edit"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("signout/", SignoutView.as_view(), name="signout"),
    path("show/<int:pk>/", UserProfileView.as_view(), name="profile"),
]