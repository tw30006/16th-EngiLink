from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from educations.models import Education
from works.models import Work
from projects.models import Project



class ResumeArea(TemplateView):
    template_name = 'resume_area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profiles = Profile.objects.filter(user=self.request.user)
        context['resumes'] = user_profiles
        context['count'] = user_profiles.count()
        return context

class ProfileListView(ListView):
    model = Profile
    template_name = 'resume/information/view.html'
    context_object_name = 'profiles' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'resume/information/create.html'
    success_url = reverse_lazy('resumes:index')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'resume/information/update.html'
    success_url = reverse_lazy('resumes:index')

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return super().form_valid(form)


class ProfileDeleteView(DeleteView):
    model = Profile
    success_url = reverse_lazy('resumes:index')



class EducationCreateView(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume/education/create.html'
    success_url = reverse_lazy('resumes:edu-show')

    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class EducationListView(ListView):
    model = Education
    template_name = 'resume/education/show.html'
    context_object_name = 'educations' 

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)


class EducationUpdateView(UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume/education/update.html'
    success_url = reverse_lazy('resumes:edu-show')
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class EducationDeleteView(DeleteView):
    model = Education
    success_url = reverse_lazy('resumes:edu-show')


class WorkCreateView(CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'resume/work/create.html'
    success_url = reverse_lazy('resumes:work-show')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    

class WorkListView(ListView):
    model = Work
    template_name = 'resume/work/show.html'
    context_object_name = 'works' 

    def get_queryset(self):
        return Work.objects.filter(profile__user=self.request.user)
    

class WorkUpdateView(UpdateView):
    model = Work
    form_class = WorkForm
    template_name = 'resume/work/update.html'
    success_url = reverse_lazy('resumes:work-show')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class WorkDeleteView(DeleteView):
    model = Work
    success_url = reverse_lazy('resumes:work-show')


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume/project/create.html'
    success_url = reverse_lazy('resumes:project-show')

    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
class ProjectListView(ListView):
    model = Project
    template_name = 'resume/project/show.html'
    context_object_name = 'projects' 

    def get_queryset(self):
        return Project.objects.filter(profile__user=self.request.user)
    
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'resume/project/update.html'
    success_url = reverse_lazy('resumes:project-show')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('resumes:project-show')



class TotalListView(ListView):
    template_name = 'resume/total.html'
    context_object_name = 'total_data'

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']

        profile_data = Profile.objects.filter(profile_id=profile_id)
        education_data = Education.objects.filter(profile_id=profile_id)
        work_data = Work.objects.filter(profile_id=profile_id)
        project_data = Project.objects.filter(profile_id=profile_id)

        total_data = {
            'education_data': education_data,
            'work_data': work_data,
            'project_data': project_data,
            'profile_data':profile_data,
        }
        return total_data

