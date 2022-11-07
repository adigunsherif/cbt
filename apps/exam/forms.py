from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from apps.core.forms import ResponsiveForm

from .models import Choice, Exam, Question


class ExamForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Exam
        exclude = ("author", "questions")


class QuestionForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Question
        exclude = ("exam",)


class QuestionChoiceForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Choice
        exclude = ("question",)


QuestionChoiceFormset = forms.modelformset_factory(
    Choice, form=QuestionChoiceForm, extra=4, max_num=5
)


QuestionUpdateChoiceFormset = forms.inlineformset_factory(
    Question,
    Choice,
    exclude=("question",),
    can_delete=True,
    widgets={
        "body": forms.Textarea(attrs={"class": "form-control mysummernote"}),
    },
)
