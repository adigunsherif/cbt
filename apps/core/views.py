from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.core.forms import (
    AcademicSessionForm,
    AcademicTermForm,
    StaffCreateForm,
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


class StudentUpdateView(OnlyAdminMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "modal_create.html"
    success_message = "User successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update student"
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class UserDeleteView(OnlyAdminMixin, DeleteView):
    model = User
    template_name = "delete.html"


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
        super().form_valid(form)
        return HttpResponse(status=204)


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


class AcademicTermCreateView(OnlyAdminMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "modal_create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new Term"
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class TermUpdateView(OnlyAdminMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "modal_create.html"
    success_message = "Term successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Term"
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)


class AcademicTermDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AcademicTerm
    template_name = "modal_delete.html"
    success_url = "/"
    success_message = "AcademicTerm successfully deleted."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class AcademicSessionCreateView(OnlyAdminMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "modal_create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class AcademicSessionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AcademicSession
    template_name = "modal_delete.html"
    success_url = "/"
    success_message = "AcademicSession successfully deleted."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "modal_create.html"
    success_message = "Session successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Session"
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)


class SubjectCreateView(OnlyAdminMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "modal_create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new subject"
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class SubjectDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Subject
    template_name = "modal_delete.html"
    success_url = "/"
    success_message = "Subject successfully deleted."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "modal_create.html"
    success_message = "Subject successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update subject"
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)


class ClassCreateView(OnlyAdminMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "modal_create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new class"
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class ClassDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StudentClass
    template_name = "modal_delete.html"
    success_url = "/"
    success_message = "Class successfully deleted."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse(status=204)


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "modal_create.html"
    success_message = "Class successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update class"
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)
