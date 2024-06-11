from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from educations.models import Education
from projects.models import Project
from works.models import Work
from .forms import ResumeForm
from .models import Resume
import json
import rules
import docraptor
import os


class ResumeArea(PermissionRequiredMixin, TemplateView):
    template_name = "resumes/area.html"
    permission_required = "user_can_show"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_resumes = Resume.objects.filter(user=self.request.user)
        context["resumes"] = user_resumes
        context["count"] = user_resumes.count()
        return context

    def get_queryset(self):
        user = self.request.user
        return Resume.objects.filter(user=user)


class ResumeListView(DetailView):
    model = Resume
    template_name = "resumes/index.html"
    context_object_name = "resume"

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get("pk")
        resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule("is_resume_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = get_object_or_404(Resume, pk=self.kwargs["pk"])
        context["resume"] = resume
        context["total_data"] = {
            "resume_data": [resume],
            "education_data": Education.edu_objects.filter(resume_id=resume.resume_id),
            "work_data": resume.works.all(),
            "project_data": resume.projects.all(),
        }
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = "resumes/create.html"
    success_url = reverse_lazy("resumes:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        print(self.request.user)
        print("6" * 100)
        form.instance.user = self.request.user
        messages.success(self.request, "新增成功")
        return super().form_valid(form)


class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = "resumes/update.html"
    success_url = reverse_lazy("resumes:index")

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get("pk")
        resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule("is_resume_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.save()
        messages.success(self.request, "更新成功")
        return super().form_valid(form)


class ResumeDeleteView(DeleteView):
    model = Resume
    success_url = reverse_lazy("resumes:index")

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get("pk")
        resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule("is_resume_user", request.user, resume):
            return HttpResponseForbidden()
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, "刪除成功")
        return response


class TotalListView(ListView):
    context_object_name = "total_data"

    def dispatch(self, request, *args, **kwargs):
        resume_id = self.kwargs.get("resume_id")
        resume = get_object_or_404(Resume, pk=resume_id)
        if not rules.test_rule("is_resume_user", request.user, resume):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return ["resumes/base_template.html"]

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

        resume = get_object_or_404(Resume, pk=resume_id, user=user)
        education_data = Education.edu_objects.filter(resume_id=resume.resume_id)
        work_data = Work.objects.filter(resume_id=resume_id).order_by("posit")
        project_data = Project.objects.filter(resume_id=resume_id).order_by("posit")

        context["total_data"] = {
            "resume_data": [resume],
            "education_data": education_data,
            "work_data": work_data,
            "project_data": project_data,
        }
        context["is_total_page"] = True

        if self.request.user.user_type == 1:
            context["base_template"] = "frontend.html"
        elif self.request.user.user_type == 2:
            context["base_template"] = "backend.html"

        context["style_template"] = f"resumes/style{resume.style}.html"
        return context


def generate_pdf_1(request, resume_id):
    docraptor_client = docraptor.DocApi()
    docraptor_client.api_client.configuration.username = os.getenv("DOCRAPTOR_API_KEY")

    resume = get_object_or_404(Resume, pk=resume_id)
    user = resume.user

    total_data = {
        "resume_data": [resume],
        "education_data": Education.objects.filter(resume=resume),
        "work_data": Work.objects.filter(resume=resume),
        "project_data": Project.objects.filter(resume=resume),
    }

    html_string = render_to_string(
        "pdf_template1.html", {"user": user, "total_data": total_data}
    )

    response = docraptor_client.create_doc(
        {
            "document_content": html_string,
            "name": f"resume_{user.username}.pdf",
            "document_type": "pdf",
            "test": os.getenv("DOCRAPTOR_TEST")
        }
    )

    pdf_response = HttpResponse(response, content_type="application/pdf")
    pdf_response["Content-Disposition"] = (
        f'attachment; filename="resume_{user.username}.pdf"'
    )

    return pdf_response


def generate_pdf_2(request, resume_id):
    docraptor_client = docraptor.DocApi()
    docraptor_client.api_client.configuration.username = os.getenv("DOCRAPTOR_API_KEY")

    resume = get_object_or_404(Resume, pk=resume_id)
    user = resume.user

    total_data = {
        "resume_data": [resume],
        "education_data": Education.objects.filter(resume=resume),
        "work_data": Work.objects.filter(resume=resume),
        "project_data": Project.objects.filter(resume=resume),
    }

    html_string = render_to_string(
        "pdf_template2.html", {"user": user, "total_data": total_data}
    )

    response = docraptor_client.create_doc(
        {
            "document_content": html_string,
            "name": f"resume_{user.username}.pdf",
            "document_type": "pdf",
            "test": os.getenv("DOCRAPTOR_TEST")
        }
    )

    pdf_response = HttpResponse(response, content_type="application/pdf")
    pdf_response["Content-Disposition"] = (
        f'attachment; filename="resume_{user.username}.pdf"'
    )

    return pdf_response


def generate_pdf_3(request, resume_id):
    docraptor_client = docraptor.DocApi()
    docraptor_client.api_client.configuration.username = os.getenv("DOCRAPTOR_API_KEY")

    resume = get_object_or_404(Resume, pk=resume_id)
    user = resume.user

    total_data = {
        "resume_data": [resume],
        "education_data": Education.objects.filter(resume=resume),
        "work_data": Work.objects.filter(resume=resume),
        "project_data": Project.objects.filter(resume=resume),
    }

    html_string = render_to_string(
        "pdf_template3.html", {"user": user, "total_data": total_data}
    )

    response = docraptor_client.create_doc(
        {
            "document_content": html_string,
            "name": f"resume_{user.username}.pdf",
            "document_type": "pdf",
            "test": os.getenv("DOCRAPTOR_TEST")
        }
    )

    pdf_response = HttpResponse(response, content_type="application/pdf")
    pdf_response["Content-Disposition"] = (
        f'attachment; filename="resume_{user.username}.pdf"'
    )

    return pdf_response


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


class UpdateStyleView(DetailView):
    model = Resume
    template_name = "resumes/update_style.html"
    context_object_name = "resume"
    pk_url_kwarg = "resume_id"


def update_template(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    if request.method == "POST":
        selected_style = request.POST.get("style")
        resume.style = selected_style
        resume.save()

        response = HttpResponse()
        response["HX-Redirect"] = reverse("resumes:total", args=[resume.pk])
        return response

    return render(request, f"resumes/style{resume.style}.html", {"resume": resume})
