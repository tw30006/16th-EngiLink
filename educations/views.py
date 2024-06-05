from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import EducationForm
from .models import Education


class EducationCreateView(PermissionRequiredMixin,CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'educations/create.html'
    permission_required = "user_can_show"

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
    success_url = reverse_lazy("resumes:educations")

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        self.object = form.save()
        return super().form_valid(form)


class EducationDeleteView(DeleteView):
    model = Education
    success_url = reverse_lazy("resumes:educations")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "刪除成功")
        return super().dispatch(request, *args, **kwargs)
