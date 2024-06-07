from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

class CustomTemplateView(TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 2:
                return redirect(reverse_lazy('companies:applications', kwargs={'pk': request.user.pk}))
            elif request.user.user_type == 1:
                return redirect(reverse_lazy('users:home'))
        return super().dispatch(request, *args, **kwargs)
