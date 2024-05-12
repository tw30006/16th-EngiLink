from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Education
from .forms import EducationForm

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

