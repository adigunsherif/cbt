from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxInput, Textarea

from .models import AmbassadorRank, RankingSession, Subject, User, Chapter


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
            "chapter",
            "ambassador_rank",
            "password1",
            "password2",
        ]



class UserUpdateForm(forms.ModelForm, ResponsiveForm):
    new_password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "ambassador_rank",
            "new_password",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get("new_password")
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
            "chapter",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_staff = True
        instance.save()
        return instance


class StaffUpdateForm(forms.ModelForm, ResponsiveForm):
    new_password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "gender",
            "chapter",
            "new_password",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get("new_password")
        if password:
            instance.set_password(password)
        if commit:
            instance.save()
        return instance


class RankingSessionForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = RankingSession
        exclude = ()


# class AcademicTermForm(forms.ModelForm, ResponsiveForm):
#     class Meta:
#         model = AcademicTerm
#         exclude = ()


class SubjectForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Subject
        exclude = ()


class AmbassadorRankForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = AmbassadorRank
        exclude = ()


class SubjectUpdateForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Subject
        exclude = ()

class ChapterCreateForm(forms.ModelForm, ResponsiveForm):
    class Meta:
        model = Chapter
        exclude = ()

