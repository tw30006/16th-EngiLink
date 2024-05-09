from django.urls import path, include
from .views import IndexView, SignUpView, ProfileUpdateView, ProfileView, LogInView, LogOutView
from jobs import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('jobs/', views.IndexView.as_view(), name='jobs'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('edit/', ProfileUpdateView.as_view(), name='edit'),
    path('show/<pk>/', ProfileView.as_view(), name='profile'),
]