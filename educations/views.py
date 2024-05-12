from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Educations
from .forms import EducationsForm

class EducationsCreateView(CreateView):
    model = Educations
    form_class = EducationsForm
    template_name = 'resume/my_education/create_education.html'
    success_url = reverse_lazy('resumes:edu-show')

    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class EducationsListView(ListView):
    model = Educations
    template_name = 'resume/my_education/show_education.html'
    context_object_name = 'educations' 

    def get_queryset(self):
        return Educations.objects.filter(profile__user=self.request.user)


class EducationsUpdateView(UpdateView):
    model = Educations
    form_class = EducationsForm
    template_name = 'resume/my_education/update_education.html'
    success_url = reverse_lazy('resumes:edu-show')
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class EducationsDeleteView(DeleteView):
    model = Educations
    success_url = reverse_lazy('resumes:edu-show')

