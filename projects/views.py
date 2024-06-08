from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.mixins import PermissionRequiredMixin
import rules
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from resumes.models import Resume

class ProjectCreateView(PermissionRequiredMixin,CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create.html'
    success_url = reverse_lazy('resumes:projects')
    permission_required = "user_can_show"

    def dispatch(self, request, *args, **kwargs):
            resume_id = self.kwargs.get('pk')
            self.resume = get_object_or_404(Resume, pk=resume_id)
            if not rules.test_rule('is_project_user',request.user, self.resume):
                return HttpResponseForbidden()
            return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.resume = self.resume
        messages.success(self.request, "新增成功")
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

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        resume = project.resume
        if not rules.test_rule("is_project_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resumes:projects', kwargs={'pk': self.object.resume.pk})

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("resumes:project-show")

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        resume = project.resume
        if not rules.test_rule("is_project_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "刪除成功")
        return response

    def get_success_url(self):
        return reverse_lazy('resumes:projects', kwargs={'pk': self.object.resume.pk})
