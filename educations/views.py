from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Education
from resumes.models import Resume
from .forms import EducationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
import rules

class EducationCreateView(PermissionRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'educations/create.html'
    permission_required = "user_can_show"

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get('pk')
        self.resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule('is_education_user',request.user, self.resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Education.objects.filter(resume_id=resume_id)

    def form_valid(self, form):
        messages.success(self.request, "新增成功")
        self.object = form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        resume_id = self.kwargs['pk']
        return reverse('resumes:educations', kwargs={'pk': resume_id})


class EducationListView(PermissionRequiredMixin, ListView):
    model = Education
    template_name = "educations/index.html"
    context_object_name = "educations"
    permission_required = "user_can_show"

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get('pk')
        self.resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule('is_education_user',request.user, self.resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Education.objects.filter(resume_id=resume_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context


class EducationUpdateView(UpdateView):
    model = Education
    form_class = EducationForm
    template_name = "educations/update.html"

    def dispatch(self, request, *args, **kwargs):
        education = self.get_object()
        resume = education.resume
        if not rules.test_rule("is_education_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('resumes:educations', kwargs={'pk': self.object.resume.pk})

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        self.object = form.save()
        return super().form_valid(form)


class EducationDeleteView(DeleteView):
    model = Education
    success_url = reverse_lazy("resumes:educations")

    def dispatch(self, request, *args, **kwargs):
        education = self.get_object()
        resume = education.resume
        if not rules.test_rule("is_education_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "刪除成功")
        return response

    def get_success_url(self):
        return reverse_lazy('resumes:educations', kwargs={'pk': self.object.resume.pk})