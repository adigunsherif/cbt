import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, View
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)

from apps.core.forms import (
    AcademicSessionForm,
    AcademicTermForm,
    StaffCreateForm,
    StaffUpdateForm,
    StudentClassForm,
    SubjectForm,
    UserCreateForm,
    UserUpdateForm,
)
from apps.core.models import AcademicSession, AcademicTerm
from apps.exam.models import Exam

from .models import StudentClass, Subject, User


class OnlyAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Helper mixin to restrict view access to admin only"""

    def test_func(self):
        return self.request.user.is_superuser


class StaffAndAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Helper mixin to restrict view access to admin and staff only"""

    def test_func(self):
        return self.request.user.is_staff


# Create your views here.
class HtmxSuccessRedirectMixin(SuccessMessageMixin):
    jsAction = "showAlert"  # or fireButton
    idToFire = None  #
    is_used_for_modal = True

    def get_id_to_fire(self):
        return self.idToFire

    def get_success_url(self):
        if self.request.POST.get("next"):
            return self.request.POST.get("next")
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return "/"

    def form_valid(self, form):
        if not self.is_used_for_modal:
            return super().form_valid(form)

        super().form_valid(form)
        redirect_url = self.get_success_url()
        response = HttpResponse()
        response["HX-Trigger"] = json.dumps(
            {
                self.jsAction: {
                    "message": self.success_message,
                    "redirect_url": redirect_url,
                    "idToFire": self.get_id_to_fire(),
                }
            }
        )
        return response


class CustomCreateView(HtmxSuccessRedirectMixin, CreateView):
    """Helper create view"""

    page_title = None
    template_name = "modal_create.html"

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_page_title()
        return context


class CustomUpdateView(HtmxSuccessRedirectMixin, UpdateView):
    """Helper update view"""

    page_title = None
    template_name = "modal_create.html"

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_page_title() or self.object
        return context


class CustomDeleteView(HtmxSuccessRedirectMixin, DeleteView):
    """Helper delete view"""

    template_name = "modal_delete.html"
    page_title = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_page_title() or self.object
        return context


class CustomFormView(HtmxSuccessRedirectMixin, FormView):
    """Helper create view"""

    page_title = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_page_title()
        return context


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        query = Exam.objects.select_related(
            "class_group", "session", "term", "subject", "author"
        )
        if user.is_superuser:
            return self.admin_page(query)
        elif user.is_staff:
            return self.staff_page(query)
        return self.student_page(query)

    def admin_page(self, query):
        paginator = Paginator(query, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"exams": page_obj}
        return render(self.request, "admin.html", context)

    def staff_page(self, query):
        paginator = Paginator(query.filter(author=self.request.user), 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"exams": page_obj}
        return render(self.request, "admin.html", context)

    def student_page(self, query):
        exams = query.filter(
            class_group=self.request.user.student_class, published=True
        )
        context = {"exams": exams}
        return render(self.request, "dashboard.html", context)


class StudentListView(OnlyAdminMixin, ListView):
    """Student Listview"""

    queryset = User.objects.filter(is_staff=False)
    template_name = "core/student_list.html"


class StudentCreateView(OnlyAdminMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "modal_create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new student"
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class StudentUpdateView(OnlyAdminMixin, CustomUpdateView):
    model = User
    form_class = UserUpdateForm
    success_message = "User successfully updated."


class UserDeleteView(OnlyAdminMixin, CustomDeleteView):
    model = User


class StaffListView(OnlyAdminMixin, ListView):
    queryset = User.objects.filter(is_staff=True)
    template_name = "core/staff_list.html"


class StaffCreateView(OnlyAdminMixin, CreateView):
    model = User
    form_class = StaffCreateForm
    template_name = "modal_create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new staff"
        return context

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({"success": True}, status=200)

    def form_invalid(self, form):
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]
        return JsonResponse({"success": False, "errors": errors}, status=400)


class StaffUpdateView(OnlyAdminMixin, CustomUpdateView):
    model = User
    form_class = StaffUpdateForm
    success_message = "User successfully updated."
    page_title = "Update Staff"


class TermSessionView(OnlyAdminMixin, View):
    template_name = "core/term_session_list.html"

    def get(self, request):
        context = {
            "terms": AcademicTerm.objects.all(),
            "sessions": AcademicSession.objects.all(),
            "subjects": Subject.objects.all(),
            "classes": StudentClass.objects.all(),
        }
        return render(request, self.template_name, context)


class AcademicTermCreateView(OnlyAdminMixin, CustomCreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = "/"
    page_title = "Add new Term"


class TermUpdateView(OnlyAdminMixin, CustomUpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_message = "Term successfully updated."
    page_title = "Update Term"


class AcademicTermDeleteView(LoginRequiredMixin, CustomDeleteView):
    model = AcademicTerm
    success_url = "/"
    success_message = "AcademicTerm successfully deleted."


class AcademicSessionCreateView(OnlyAdminMixin, CustomCreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = "/"
    page_title = "Add new Session"


class AcademicSessionDeleteView(LoginRequiredMixin, CustomDeleteView):
    model = AcademicSession
    template_name = "modal_delete.html"
    success_url = "/"
    success_message = "AcademicSession successfully deleted."


class SessionUpdateView(LoginRequiredMixin, CustomUpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_message = "Session successfully updated."
    page_title = "Update Session"


class SubjectCreateView(OnlyAdminMixin, CustomCreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "modal_create.html"
    success_url = "/"
    page_title = "Add new Subject"


class SubjectDeleteView(LoginRequiredMixin, CustomDeleteView):
    model = Subject
    success_url = "/"
    success_message = "Subject successfully deleted."


class SubjectUpdateView(LoginRequiredMixin, CustomUpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "modal_create.html"
    success_message = "Subject successfully updated."
    page_title = "Update Subject"


class ClassCreateView(OnlyAdminMixin, CustomCreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "modal_create.html"
    success_url = "/"
    page_title = "Add new Class"


class ClassDeleteView(LoginRequiredMixin, CustomDeleteView):
    model = StudentClass
    success_url = "/"
    success_message = "Class successfully deleted."


class ClassUpdateView(LoginRequiredMixin, CustomUpdateView):
    model = StudentClass
    form_class = StudentClassForm
    success_message = "Class successfully updated."
    page_title = "Update Class"


# ERRORS
def error_404(request, exception):
    return render(request, "error/404.html", status=404)


def error_500(request):
    return render(request, "error/500.html", status=500)


def error_503(request):
    return render(request, "error/503.html", status=503)


def error_401(request, exception=None):
    return render(request, "error/401.html", status=401)


def error_403(request, exception=None):
    return render(request, "error/403.html", status=403)
