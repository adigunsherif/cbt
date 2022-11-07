""" Not used for now . backup classes """

from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from apps.core.forms import ResponsiveForm

from ..apps.exam.models import Choice, Exam, Question


class ExamForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Exam
        exclude = ("author", "questions")


ChoiceFormset = forms.inlineformset_factory(
    Question,
    Choice,
    exclude=("question",),
    extra=4,
    max_num=5,
    can_delete=True,
    widgets={
        "body": forms.Textarea(attrs={"class": "form-control mysummernote"}),
    },
)


def is_empty_form(form):
    """
    A form is considered empty if it passes its validation,
    but doesn't have any data.
    This is primarily used in formsets, when you want to
    validate if an individual form is empty (extra_form).
    """
    if form.is_valid() and not form.cleaned_data:
        return True
    else:
        # Either the form has errors (isn't valid) or
        # it doesn't have errors and contains data.
        return False


def is_form_persisted(form):
    """
    Does the form have a model instance attached and it's not being added?
    e.g. The form is about an existing Book whose data is being edited.
    """
    if form.instance and not form.instance._state.adding:
        return True
    else:
        # Either the form has no instance attached or
        # it has an instance that is being added.
        return False


class BaseQuestionsForm(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a question's choices in the nested property.
        form.nested = ChoiceFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix="questionchoice-%s-%s"
            % (form.prefix, ChoiceFormset.get_default_prefix()),
        )

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the Book form is empty, but there are Images.
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, "nested") or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(
                        "You are trying to add choices to a question which "
                        "does not yet exist. Please add question and choose add the choices again."
                    ),
                )

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Images to a new Book whose data we haven't entered?
        """
        if not hasattr(form, "nested"):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


"""
ExamQuestionChoice = forms.inlineformset_factory(
    Exam,
    Question,
    formset=BaseQuestionsForm,
    fields=("question",),
    can_delete=True,
    # widgets={
    #   "question": CKEditorUploadingWidget(attrs={"class": "form-control", #"rows": 2}),
    # },
) """


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
