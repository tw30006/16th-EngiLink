from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume/my_project/create_project.html'
    success_url = reverse_lazy('resumes:project-show')

    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
class ProjectListView(ListView):
    model = Project
    template_name = 'resume/my_project/show_project.html'
    context_object_name = 'projects' 

    def get_queryset(self):
        return Project.objects.filter(profile__user=self.request.user)
    
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume/my_project/update_project.html'
    success_url = reverse_lazy('resumes:project-show')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('resumes:project-show')
