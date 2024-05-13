from .forms import WorkForm
from .models import Work
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView



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
