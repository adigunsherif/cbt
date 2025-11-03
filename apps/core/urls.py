from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("students/", views.AmbassadorListView.as_view(), name="student_list"),
    path("students/create/", views.AmbassadorCreateView.as_view(), name="student_create"),
    path(
        "students/<int:pk>/update/",
        views.AmbassadorUpdateView.as_view(),
        name="student-update",
    ),
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
    path("staff/create/", views.StaffCreateView.as_view(), name="staff_create"),
    path(
        "staff/<int:pk>/update/",
        views.StaffUpdateView.as_view(),
        name="staff-update",
    ),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("termsession/", views.TermSessionView.as_view(), name="term_session"),

    path(
        "session/create/",
        views.RankingSessionCreateView.as_view(),
        name="session_create",
    ),
    path(
        "session/delete/<int:pk>/",
        views.RankingSessionDeleteView.as_view(),
        name="rankingsession_delete",
    ),
    path(
        "session/<int:pk>/update/",
        views.RankingSessionUpdateView.as_view(),
        name="session_update",
    ),
    path(
        "subject/create/",
        views.SubjectCreateView.as_view(),
        name="subject_create",
    ),
    path(
        "subject/delete/<int:pk>/",
        views.SubjectDeleteView.as_view(),
        name="subject_delete",
    ),
    path(
        "subject/<int:pk>/update/",
        views.SubjectUpdateView.as_view(),
        name="subject_update",
    ),
    path(
        "class/create/",
        views.RankCreateView.as_view(),
        name="rank_create",
    ),
    path(
        "class/delete/<int:pk>/",
        views.RankDeleteView.as_view(),
        name="rank_delete",
    ),
    path(
        "class/<int:pk>/update/",
        views.RankUpdateView.as_view(),
        name="rank_update",
    ),
    path(
        "chapter/create/",
        views.ChapterCreateVuew.as_view(),
        name="chapter_create"
    )
]