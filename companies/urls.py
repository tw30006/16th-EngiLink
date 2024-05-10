from django.urls import path
from .views import IndexView, SignUpView, UpdateView, ShowView, LogInView, LogOutView
from jobs import views as jobs

app_name = "companies"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('update/', UpdateView.as_view(), name='update'),
    path('<pk>/jobs/', jobs.IndexView.as_view(), name="jobs"),
    path('<pk>/create/', jobs.AddView.as_view(), name="jobs_create"),
    path('<pk>/', ShowView.as_view(), name='show'),
]