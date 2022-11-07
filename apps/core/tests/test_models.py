from django.test import TestCase

from apps.core.models import StudentClass, Subject, User


class UserTest(TestCase):
    def test_str(self):
        user = User.objects.create(
            username="TestUser",
            fullname="Test",
            password="pass",
            is_superuser=True,
            is_staff=True,
        )
        self.assertEqual(user.__str__(), "Test")


class SubjectTest(TestCase):
    def test_str(self):
        subject = Subject.objects.create(name="test_subject", code="123")
        self.assertEqual(subject.__str__(), "test_subject")


class StudentClassTest(TestCase):
    def test_str(self):
        student_class = StudentClass.objects.create(name="test_class", code="AA11")
        self.assertEqual(student_class.__str__(), "test_class")
