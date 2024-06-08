from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import WorkForm
from .models import Work
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from resumes.models import Resume
import rules


class WorkCreateView(PermissionRequiredMixin, CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'works/create.html'
    permission_required = "user_can_show"

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get('pk')
        self.resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule('is_work_user',request.user, self.resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Work.objects.filter(resume_id=resume_id)
    
    def form_valid(self, form):
        form.instance.resume = self.resume
        messages.success(self.request, "新增成功")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        resume_id = self.kwargs['pk']
        return reverse('resumes:works', kwargs={'pk': resume_id})


class WorkListView(PermissionRequiredMixin, ListView):
    model = Work
    template_name = "works/index.html"
    context_object_name = "works"
    permission_required = "user_can_show"

    def dispatch(self, request, *args, **kwargs):
            resume_id = self.kwargs.get('pk')
            self.resume = get_object_or_404(Resume, pk=resume_id)
            if not rules.test_rule('is_work_user',request.user, self.resume):
                return HttpResponseForbidden()
            return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Work.objects.filter(resume_id=resume_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context

class WorkUpdateView(UpdateView):
    model = Work
    form_class = WorkForm
    template_name = "works/update.html"
    success_url = reverse_lazy("resumes:work-show")

    def dispatch(self, request, *args, **kwargs):
        work = self.get_object()
        resume = work.resume
        if not rules.test_rule("is_work_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resumes:works', kwargs={'pk': self.object.resume.pk})


class WorkDeleteView(DeleteView):
    model = Work
    success_url = reverse_lazy("resumes:work-show")

    def dispatch(self, request, *args, **kwargs):
        work = self.get_object()
        resume = work.resume
        if not rules.test_rule("is_work_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "刪除成功")
        return reverse_lazy('resumes:works', kwargs={'pk': self.object.resume.pk})

