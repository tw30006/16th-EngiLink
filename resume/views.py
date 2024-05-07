from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import get_object_or_404

class ResumeArea(TemplateView):
    template_name = 'resume_area.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Profile.objects.all()
        context['count'] = Profile.objects.count()
        return context

class ProfileListView(ListView):
    model = Profile
    template_name = 'my_information/view_information.html'
    context_object_name = 'profiles' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'my_information/create_information.html'
    success_url = reverse_lazy('resumes:index')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'my_information/update_information.html'
    success_url = reverse_lazy('resumes:index')

    def form_valid(self, form):
        # 將更改應用到資料庫
        self.object = form.save()
        return super().form_valid(form)
    
class ProfileDeleteView(DeleteView):
    model = Profile
    success_url = reverse_lazy('resumes:index')

