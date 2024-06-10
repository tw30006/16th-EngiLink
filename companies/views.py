from django.contrib import messages
from django.contrib.auth import logout, login, get_backends
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Template, Context
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView
from jobs.models import Job_Resume, Job, User_Job
from .models import Company, User_Company
from .forms import CompanyRegisterForm, CompanyUpdateForm
from django.contrib.auth.models import AnonymousUser
import rules


def get_user_backend(user):
    for backend in get_backends():
        if backend.get_user(user.pk) is not None:
            return backend
    raise Exception("No backend found for user")


class CompanyRegisterView(FormView):
    template_name = "companies/register.html"
    form_class = CompanyRegisterForm

    def form_valid(self, form):
        user = form.save()
        backend = get_user_backend(user)
        messages.success(self.request, "註冊成功")
        login(
            self.request,
            user,
            backend=backend.__module__ + "." + backend.__class__.__name__,
        )
        return super(CompanyRegisterView, self).form_valid(form)

    def get_success_url(self):
        user = self.request.user

        try:
            company = Company.objects.get(custom_user=user)
        except Company.DoesNotExist:
            company = None

        if user.user_type == 2 and company is None:
            return reverse_lazy("users:create", kwargs={"pk": user.pk})
        else:
            return reverse_lazy("companies:home")


class CompanyHomeView(PermissionRequiredMixin, TemplateView):
    model = Company
    template_name = "companies/home.html"
    permission_required = "company_can_show"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(custom_user=self.request.user)
        context["company"] = company
        return context

class CompanyLoginView(LoginView):
    template_name = "companies/login.html"   
    
    def form_invalid(self, form):
        messages.error(self.request, "登入失敗")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.success(self.request, "登入成功")
        return super().form_valid(form)
        

    def get_default_redirect_url(self):
        user = self.request.user

        try:
            company = Company.objects.get(custom_user=user)
        except Company.DoesNotExist:
            company = None

        if user.user_type == 2 and company is None:
            return reverse_lazy("users:create", kwargs={"pk": user.pk})

        elif user.user_type == 1:
            logout(self.request)
            return reverse_lazy("users:login")

        else:
            return reverse_lazy("companies:home")


class CompanyLogoutView(PermissionRequiredMixin, LogoutView):
    next_page = reverse_lazy("home")
    permission_required = "company_can_show"

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "登出成功")
        return super().dispatch(request, *args, **kwargs)


class CompanyDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Company
    template_name = "companies/detail.html"
    context_object_name = "company"
    login_url = "/companies/"
    permission_required = "company_can_show"

    def dispatch(self, request, *args, **kwargs):
        self.company = self.get_object()
        if not rules.test_rule("is_current_company", request.user, self.company):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object.custom_user
        context["description"] = self.object.description
        return context


class CompanyUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "companies/update.html"
    context_object_name = "company"
    success_url = "/companies/"
    login_url = "/companies/"
    permission_required = "company_can_show"

    def get_queryset(self):
        user = self.request.user
        queryset = Company.objects.filter(custom_user=user, custom_user__user_type=2)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.object
        context["user"] = self.object.custom_user
        return context

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        return super().form_valid(form)

class CompanyPasswordChangeView(PermissionRequiredMixin, PasswordChangeView):
    template_name = "companies/password_change_form.html"
    success_url = "/companies/"
    permission_required = "company_can_show"

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("companies:login"))
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "更新成功")
        response = super().form_valid(form)
        logout(self.request)
        return response


class CompanyListView(ListView):
    model = Company
    template_name = "companies/list.html"
    context_object_name = "companies_list"

    def get_queryset(self):
        queryset = Company.objects.all()
        search_keyword = self.request.GET.get("q")
        if search_keyword:
            queryset = queryset.filter(company_name__icontains=search_keyword)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            favorite_company_ids = User_Company.objects.filter(
                user=self.request.user, collect=True
            ).values_list("company_id", flat=True)
            context["favorite_company_ids"] = favorite_company_ids
        else:
            context["favorite_company_ids"] = []
        return context


class CompanyInfoView(DetailView):
    model = Company
    template_name = "companies/info.html"
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["location"] = self.object.address[:3]
        context["address"] = self.object.address[3:]
        context["job_count"] = self.object.jobs.count()
        context["jobs"] = self.object.jobs.all()

        if isinstance(self.request.user, AnonymousUser):
            context["user_jobs"] = []
        else:
            collected_jobs = User_Job.objects.filter(user=self.request.user).values_list('job_id', flat=True)
            context["user_jobs"] = list(collected_jobs)
            
        return context


class JobApplicationsView(ListView):
    model = Job_Resume
    template_name = "companies/apply.html"

    def get_queryset(self):
        company = get_object_or_404(Company, custom_user=self.request.user)
        return Job_Resume.objects.filter(job__company=company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, custom_user=self.request.user)
        company_jobs = Job.objects.filter(company=company)
        job_resume_dict = {}
        for job in company_jobs:
            job_resume_dict[job] = Job_Resume.objects.filter(job=job)
        context["job_resume_dict"] = job_resume_dict
        context["company"] = self.request.user.company
        return context

    def form_valid(self, form):
        job_resume_id = self.request.POST.get("job_resume_id")
        job_resume = get_object_or_404(Job_Resume, pk=job_resume_id)

        interview_date = form.cleaned_data["interview_date"]
        interview_invitation = form.cleaned_data["interview_invitation"]

        invitation_template = Template(interview_invitation)
        context = Context(
            {
                "job_resume": job_resume,
                "interview_date": interview_date,
                "company": self.request.user.company,
            }
        )
        job_resume.interview_invitation = invitation_template.render(context)
        job_resume.interview_date = interview_date
        job_resume.save()
        return super().form_valid(form)


class JobApplicationDetailView(DetailView):
    model = Job_Resume
    context_object_name = "company"


    def get_template_names(self):
        return ["resumes/base_template.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_resume = self.get_object()
        resume = job_resume.resume
        resume_data = [resume]
        education_data = resume.educations.all()
        work_data = resume.works.all()
        project_data = resume.projects.all()

        context["total_data"] = {
            "resume_data": resume_data,
            "education_data": education_data,
            "work_data": work_data,
            "project_data": project_data,
        }

        if self.request.user.user_type == 1:
            context["base_template"] = "frontend.html"
        elif self.request.user.user_type == 2:
            context["base_template"] = "backend.html"

        context["style_template"] = f"resumes/style{resume.style}.html"
        
        return context


class MarkAsReadView(View):
    def post(self, request, *args, **kwargs):
        job_resume_id = self.kwargs.get("pk")
        job_resume = get_object_or_404(Job_Resume, id=job_resume_id)
        if request.user == job_resume.job.company.custom_user:
            job_resume.read_at = timezone.now()
            job_resume.save()
        return redirect("companies:applications", pk=job_resume.job.company_id)


class InterviewResultCreateView(View):
    def post(self, request, job_resume_id, *args, **kwargs):
        interview_date = request.POST.get("interview_date")
        interview_invitation = request.POST.get("interview_invitation")
        job_resume = Job_Resume.objects.get(pk=job_resume_id)
        job_resume.interview_date = interview_date
        job_resume.interview_invitation = interview_invitation
        job_resume.save()
        messages.success(self.request, "發送成功")
        return redirect("companies:home")


class CompanyInterviewsCalendarView(View):
    def get(self, request):
        company_user = request.user 
        interviews = Job_Resume.objects.filter(
            job__company=company_user.company,  
            interview_date__isnull=False,
            accepted="accept"
        )

        context = {"interviews": interviews}
        return render(request, "companies/calendar.html", context)

class FavoriteCompanyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        company = get_object_or_404(Company, id=self.kwargs["company_id"])
        user_company, created = User_Company.objects.get_or_create(
            company=company, user=request.user
        )
        if user_company.collect:
            user_company.collect = False
            messages.success(request, "已取消收藏公司")
        else:
            user_company.collect = True
            messages.success(request, "已收藏公司")
        user_company.save()
        return redirect(request.META.get("HTTP_REFERER", "companies:company_list"))


class CollectCompanyView(LoginRequiredMixin, View):
    def post(self, request):
        company_id = request.POST.get("company_id")
        company = get_object_or_404(Company, id=company_id)
        user_company = User_Company.objects.filter(user=request.user, company=company)
        if user_company.exists():
            user_company.delete()
        else:
            user_company = User_Company.objects.create(
                company=company, user=request.user
            )

        if "HX-Request" in request.headers:
            user_companies = User_Company.objects.filter(
                user=request.user, collect=True
            ).values_list("company_id", flat=True)
            button_html = render_to_string(
                "shared/collect_btn.html",
                {"company": company, "user_companies": user_companies},
            )
            return HttpResponse(button_html)
        return redirect("users:home")

    def get(self, request):
        companies = Company.objects.all()
        user_companies = User_Company.objects.filter(
            user=request.user, collect=True
        ).values_list("company_id", flat=True)
        user_jobs = User_Job.objects.filter(user=request.user).values_list(
            "job_id", flat=True
        )
        jobs = Job.objects.select_related("company").all()
        return render(
            request,
            "users/collect.html",
            {
                "companies": companies,
                "user_companies": user_companies,
                "jobs": jobs,
                "user_jobs": user_jobs,
            },
        )
