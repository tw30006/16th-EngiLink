from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ProjectCreateView(PermissionRequiredMixin,CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create.html'
    success_url = reverse_lazy('resumes:projects')
    permission_required = "user_can_show"

    def form_valid(self, form):
        messages.success(self.request, "新增成功")
        self.object = form.save()
        return super().form_valid(form)
    
    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Project.objects.filter(resume_id=resume_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        resume_id = self.kwargs['pk']
        return reverse('resumes:projects', kwargs={'pk': resume_id})
    
class ProjectListView(PermissionRequiredMixin,ListView):
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'projects' 
    permission_required = "user_can_show"

    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Project.objects.filter(resume_id=resume_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/update.html"
    success_url = reverse_lazy("resumes:project-show")


    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        self.object = form.save()
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("resumes:project-show")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "刪除成功")
        return super().dispatch(request, *args, **kwargs)
