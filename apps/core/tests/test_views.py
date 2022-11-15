from django.test import TestCase
from django.urls import reverse

from apps.core.models import Gender, User


class DashboardViewTest(TestCase):
    def test_admin_dashboard(self):
        admin = User.objects.get(pk=1)
        self.client.force_login(admin)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_student_dashboard(self):
        student = User.objects.create_user(
            username="john", password="doe", gender=Gender.MALE
        )
        self.client.force_login(student)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_unauthenticated_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/")
