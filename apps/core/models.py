from django.contrib.auth.models import AbstractUser
from django.db import models


class Gender:
    MALE = "male"
    FEMALE = "female"
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]


class User(AbstractUser):
    """Extends the user's table"""

    gender = models.CharField(choices=Gender.GENDER_CHOICES, max_length=10)
    is_active = models.BooleanField(default=True)
    student_class = models.ForeignKey(
        "StudentClass", on_delete=models.SET_NULL, null=True, blank=True
    )


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    """Student class category table"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
