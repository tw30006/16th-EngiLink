from django.contrib import messages
from .forms import WorkForm
from .models import Work
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin


class WorkCreateView(PermissionRequiredMixin,CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'works/create.html'
    permission_required = "user_can_show"

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "新增成功")
        return super().form_valid(form)
    
    def get_queryset(self):
        resume_id = self.kwargs['pk']
        return Work.objects.filter(resume_id=resume_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        resume_id = self.kwargs['pk']
        return reverse('resumes:works', kwargs={'pk': resume_id})


class WorkListView(PermissionRequiredMixin,ListView):
    model = Work
    template_name = 'works/index.html'
    context_object_name = 'works' 
    permission_required = "user_can_show"

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


    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "更新成功")
        return super().form_valid(form)


class WorkDeleteView(DeleteView):
    model = Work
    success_url = reverse_lazy("resumes:work-show")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "刪除成功")
        return super().dispatch(request, *args, **kwargs)
