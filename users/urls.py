from django.urls import path
from .views import (
    UserHomeView,
    UserLoginView,
    UserLogoutView,
    UserDetailView,
    UserUpdateView,
    UserRegisterView,
    UserPasswordChangeView,
    UserJobsView,
    ApplyForJobCreateView,
    ApplyForJobListView,
    WithdrawApplicationView,
    CollectJobView,
    InterviewResponseView,
)
from resumes import views as resumes

app_name = "users"

urlpatterns = [
    path("", UserHomeView.as_view(), name="home"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        UserPasswordChangeView.as_view(),
        name="password_change",
    ),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<pk>/resumes/", resumes.ResumeArea.as_view(), name="resumes"),
    path('<int:job_id>/apply/', ApplyForJobCreateView.as_view(), name='apply'),
    path('<pk>/applications/', ApplyForJobListView.as_view(), name='applications'),
    path('<int:pk>/withdraw/', WithdrawApplicationView.as_view(), name='withdraw'),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("collect/", CollectJobView.as_view(), name="collect"),
    path("jobs/", UserJobsView.as_view(), name="jobs"),
    path('interview/<int:pk>/', InterviewResponseView.as_view(), name='interview'),
]

