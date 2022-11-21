from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxInput, Textarea

from .models import AcademicSession, AcademicTerm, StudentClass, Subject, User


class ResponsiveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, Textarea):
                field.widget.attrs["class"] = "form-control mysummernote "
            else:
                field.widget.attrs["class"] = "form-control"


class UserCreateForm(UserCreationForm, ResponsiveForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "gender",
            "student_class",
            "password1",
            "password2",
        ]


class UserUpdateForm(forms.ModelForm, ResponsiveForm):
    password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "gender",
            "student_class",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance


class StaffCreateForm(UserCreationForm, ResponsiveForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "gender",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_staff = True
        instance.save()
        return instance


class AcademicSessionForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = AcademicSession
        exclude = ()


class AcademicTermForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = AcademicTerm
        exclude = ()


class SubjectForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Subject
        exclude = ()


class StudentClassForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = StudentClass
        exclude = ()


class SubjectUpdateForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Subject
        exclude = ()
