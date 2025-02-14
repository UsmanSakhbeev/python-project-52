from urllib import request

import django_filters
from django.forms.widgets import CheckboxInput
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    user_own_tasks = django_filters.BooleanFilter(
        label=_("Only my own tasks"),
        widget=CheckboxInput,
        method="filter_user_own_tasks",
    )

    label = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
    )

    def filter_user_own_tasks(self, queryset, name, value):
        if value and hasattr(self, "request"):
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "label"]
