from django.urls import path
from .views import ResumeArea,ProfileListView,ProfileCreateView,ProfileUpdateView,ProfileDeleteView,EducationCreateView,EducationListView,EducationUpdateView,EducationDeleteView,WorkCreateView,WorkListView,WorkUpdateView,WorkDeleteView,ProjectCreateView,ProjectListView,ProjectUpdateView,ProjectDeleteView,TotalListView

app_name = 'resumes' 

urlpatterns = [
    path('',ResumeArea.as_view(),name='index'),
    path('create/',ProfileCreateView.as_view(),name='create'),
    path('edit/<pk>', ProfileUpdateView.as_view(), name='edit'),
    path('delete/<pk>', ProfileDeleteView.as_view(), name='delete'),
    path('edu/',EducationCreateView.as_view(),name='edu'),
    path('edu/show/',EducationListView.as_view(),name='edu-show'),
    path('edu/edit/<pk>', EducationUpdateView.as_view(), name='edu-edit'),
    path('edu/delete/<pk>', EducationDeleteView.as_view(), name='edu-delete'),
    path('work/',WorkCreateView.as_view(),name='work'),
    path('work/show/',WorkListView.as_view(),name='work-show'),
    path('work/edit/<pk>', WorkUpdateView.as_view(), name='work-edit'),
    path('work/delete/<pk>', WorkDeleteView.as_view(), name='work-delete'),
    path('project/',ProjectCreateView.as_view(),name='project'),
    path('project/show/',ProjectListView.as_view(),name='project-show'),
    path('project/edit/<pk>', ProjectUpdateView.as_view(), name='project-edit'),
    path('project/delete/<pk>', ProjectDeleteView.as_view(), name='project-delete'),
    path('<pk>/',ProfileListView.as_view(),name='show'),
    path('total/<int:profile_id>',TotalListView.as_view(),name='total'),
]