from django import forms
from django.forms import BaseInlineFormSet, ValidationError
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
        fields = ("subject", "class_group", "question")


class QuestionChoiceForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Choice
        exclude = ("question",)


class BaseChoiceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = sum(
            1
            for form in self.forms
            if form.cleaned_data.get("is_correct")
            and not form.cleaned_data.get("DELETE", False)
        )
        if correct_count != 1:
            raise ValidationError("You must mark exactly one choice as correct.")


QuestionChoiceFormset = forms.modelformset_factory(
    Choice,
    form=QuestionChoiceForm,
    extra=4,
    max_num=5,
    formset=BaseChoiceInlineFormSet,
)


QuestionUpdateChoiceFormset = forms.inlineformset_factory(
    Question,
    Choice,
    exclude=("question",),
    can_delete=True,
    widgets={
        "body": forms.Textarea(attrs={"class": "form-control mysummernote"}),
    },
    formset=BaseChoiceInlineFormSet,
)
