from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import TaskAuthorPermissionMixin
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["id"]

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["request"] = self.request
        return kwargs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Task Create"), "button_name": _("Create")}
    success_message = _("Task was created successfully")
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Task Update"), "button_name": _("Update")}
    success_message = _("Task was updated successfully")
    success_url = reverse_lazy("task_list")


class TaskDeleteView(
    LoginRequiredMixin, TaskAuthorPermissionMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "tasks/task_delete.html"
    extra_context = {"title": _("Delete Task"), "button_name": _("Yes, delete")}
    success_message = _("Task was deleted successfully")
    permission_denied_message = _("Only the task's author can delete it")
    success_url = reverse_lazy("task_list")
