from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from .forms import ProfileForm,EducationForm,WorkForm,ProjectForm
from .models import Profile,Education,Work,Project
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
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
    template_name = 'resume/my_information/view_information.html'
    context_object_name = 'profiles' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'resume/my_information/create_information.html'
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
    template_name = 'resume/my_information/update_information.html'
    success_url = reverse_lazy('resumes:index')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
class ProfileDeleteView(DeleteView):
    model = Profile
    success_url = reverse_lazy('resumes:index')




class EducationCreateView(CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume/my_education/create_education.html'
    success_url = reverse_lazy('resumes:edu-show')

    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class EducationListView(ListView):
    model = Education
    template_name = 'resume/my_education/show_education.html'
    context_object_name = 'educations' 

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)


class EducationUpdateView(UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'resume/my_education/update_education.html'
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
    template_name = 'resume/my_work/create_work.html'
    success_url = reverse_lazy('resumes:work-show')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    

class WorkListView(ListView):
    model = Work
    template_name = 'resume/my_work/show_work.html'
    context_object_name = 'works' 

    def get_queryset(self):
        return Work.objects.filter(profile__user=self.request.user)
    

class WorkUpdateView(UpdateView):
    model = Work
    form_class = WorkForm
    template_name = 'resume/my_work/update_work.html'
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

