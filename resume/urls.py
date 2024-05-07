from django.urls import path
from .views import ResumeArea,ProfileListView,ProfileCreateView,ProfileUpdateView,ProfileDeleteView

app_name = 'resumes' 

urlpatterns = [
    path('',ResumeArea.as_view(),name='index'),
    path('create/',ProfileCreateView.as_view(),name='create'),
    path('edit/<pk>', ProfileUpdateView.as_view(), name='edit'),
    path('delete/<pk>', ProfileDeleteView.as_view(), name='delete'),
    path('<pk>',ProfileListView.as_view(),name='show'),
]