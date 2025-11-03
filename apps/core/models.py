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
    ambassador_rank = models.ForeignKey(
        "AmbassadorRank", on_delete=models.SET_NULL, null=True, blank=True
    )
    chapter = models.ForeignKey("Chapter", on_delete=models.SET_NULL, blank=True, null=True)



class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AmbassadorRank(models.Model):
    """Ambassador rank table"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Ambassador Rank"
        verbose_name_plural = "Ambassador Ranks"
        ordering = ["name"]

    def __str__(self):
        return self.name


# class AcademicTerm(models.Model):
#     name = models.CharField(max_length=200, unique=True)

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


class RankingSession(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Chapter(models.Model):
    title = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]        

    def __str__(self):
        return self.title