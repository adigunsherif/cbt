import django_filters

from apps.core.forms import ResponsiveForm

from .models import Question


class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ["subject", "class_group"]
        form = ResponsiveForm
