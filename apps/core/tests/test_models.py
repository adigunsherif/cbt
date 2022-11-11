from django.test import TestCase

from apps.core.models import StudentClass, Subject, User


class SubjectTest(TestCase):
    def test_str(self):
        subject = Subject.objects.create(name="test_subject")
        self.assertEqual(subject.__str__(), "test_subject")


class StudentClassTest(TestCase):
    def test_str(self):
        student_class = StudentClass.objects.create(name="test_class")
        self.assertEqual(student_class.__str__(), "test_class")
