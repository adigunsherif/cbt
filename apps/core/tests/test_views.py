from django.test import TestCase
from django.urls import reverse

from apps.core.models import User


class DashboardViewTest(TestCase):
    def test_dashboard_template_admin(self):
        admin = User.objects.get(pk=1)
        self.client.force_login(admin)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_template_student(self):
        student = User.objects.create_user(
            username="student", password="pass", fullname="adrew"
        )
        self.client.force_login(student)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_dashboard_template_anonymous(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/")
