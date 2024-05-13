from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from .forms import ResumeForm
from .models import Resume
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from educations.models import Education
from works.models import Work
from projects.models import Project



class ResumeArea(TemplateView):
    template_name = 'resumes/area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_resumes = Resume.objects.filter(user=self.request.user)
        context['resumes'] = user_resumes
        context['count'] = user_resumes.count()
        return context

class ResumeListView(ListView):
    model = Resume
    template_name = 'resumes/index.html'
    context_object_name = 'resumes' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = get_object_or_404(Resume, pk=self.kwargs['pk'])
        context['resume'] = resume
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/create.html'
    success_url = reverse_lazy('resumes:index')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/update.html'
    success_url = reverse_lazy('resumes:index')

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.save()
        return super().form_valid(form)


class ResumeDeleteView(DeleteView):
    model = Resume
    success_url = reverse_lazy('resumes:index')


class TotalListView(ListView):
    template_name = 'resumes/total.html'
    context_object_name = 'total_data'

    def get_queryset(self):
        resume_id = self.kwargs['resume_id']

        resume_data = Resume.objects.filter(resume_id=resume_id)
        education_data = Education.objects.filter(resume_id=resume_id)
        work_data = Work.objects.filter(resume_id=resume_id)
        project_data = Project.objects.filter(resume_id=resume_id)

        total_data = {
            'education_data': education_data,
            'work_data': work_data,
            'project_data': project_data,
            'resume_data':resume_data,
        }
        return total_data

