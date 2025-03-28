from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskCreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
