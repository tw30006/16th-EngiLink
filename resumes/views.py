from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ResumeForm
from .models import Resume
from educations.models import Education
from works.models import Work
from projects.models import Project
from django.template.loader import render_to_string
from django.contrib.auth.mixins import PermissionRequiredMixin
import json
from weasyprint import HTML

class ResumeArea(PermissionRequiredMixin, TemplateView):
    template_name = "resumes/area.html"
    permission_required = "user_can_show"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_resumes = Resume.objects.filter(user=self.request.user)
        context["resumes"] = user_resumes
        context["count"] = user_resumes.count()
        return context


class ResumeListView(ListView):
    model = Resume
    template_name = "resumes/index.html"
    context_object_name = "resumes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = get_object_or_404(Resume, pk=self.kwargs["pk"])
        context["resume"] = resume
        return context


class ResumeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = "resumes/create.html"
    success_url = reverse_lazy("resumes:index")
    permission_required = "user_can_show"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "新增成功")
        return super().form_valid(form)


class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = "resumes/update.html"
    success_url = reverse_lazy("resumes:index")

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.save()
        messages.success(self.request, "更新成功")
        return super().form_valid(form)


class ResumeDeleteView(DeleteView):
    model = Resume
    success_url = reverse_lazy("resumes:index")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "刪除成功")
        return super().dispatch(request, *args, **kwargs)


class TotalListView(ListView):
    template_name = "resumes/style1.html"
    context_object_name = "total_data"

    def get_queryset(self):
        resume_id = self.kwargs["resume_id"]
        resume_data = Resume.objects.filter(resume_id=resume_id)
        education_data = Education.objects.filter(resume_id=resume_id).order_by("posit")
        work_data = Work.objects.filter(resume_id=resume_id).order_by("posit")
        project_data = Project.objects.filter(resume_id=resume_id).order_by("posit")

        total_data = {
            "education_data": education_data,
            "work_data": work_data,
            "project_data": project_data,
            "resume_data": resume_data,
        }
        return total_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_id = self.kwargs["resume_id"]
        user = self.request.user

        resume_data = Resume.objects.filter(resume_id=resume_id, user=user)
        education_data = Education.objects.filter(resume_id=resume_id).order_by("posit")
        work_data = Work.objects.filter(resume_id=resume_id).order_by("posit")
        project_data = Project.objects.filter(resume_id=resume_id).order_by("posit")

        context["total_data"] = {
            "resume_data": resume_data,
            "education_data": education_data,
            "work_data": work_data,
            "project_data": project_data,
        }
        return context


def generate_resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    user = resume.user

    total_data = {
        "resume_data": [resume],
        "education_data": Education.objects.filter(resume=resume),
        "work_data": Work.objects.filter(resume=resume),
        "project_data": Project.objects.filter(resume=resume),
    }

    html_string = render_to_string(
        "pdf_template.html", {"user": user, "total_data": total_data}
    )

    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{user.username}.pdf"'

    return response


def update_positions(request):
    if request.method == "POST":
        data = json.loads(request.body)
        positions = data.get("positions", [])

        for item in positions:
            obj_type = item.get("type")
            obj_id = int(item.get("id"))
            new_position = int(item.get("position"))

            if obj_type == "education":
                Model = Education
            elif obj_type == "work":
                Model = Work
            elif obj_type == "project":
                Model = Project
            else:
                continue

            obj = Model.objects.get(id=obj_id)
            obj.posit = new_position
            obj.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail", "error": "Invalid request method"})
