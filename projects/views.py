from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create.html"
    success_url = reverse_lazy("resumes:project-show")

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class ProjectListView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(resume__user=self.request.user)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/update.html"
    success_url = reverse_lazy("resumes:project-show")

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("resumes:project-show")
