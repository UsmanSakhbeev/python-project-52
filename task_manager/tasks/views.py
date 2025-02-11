from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.mixins import UserPermissionMixin
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["id"]


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Task Create"), "button_name": _("Create")}
    success_message = _("Task was created successfully")
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Task Uapdate"), "button_name": _("Update")}
    success_message = _("Task was created successfully")
    success_url = reverse_lazy("task_list")


class TaskDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = Task
    template_name = "users/task_delete.html"
    extra_context = {"title": _("Delete user"), "button_name": _("Delete")}
    success_message = _("User was deleted succesfully")
    permission_denied_message = _("Only the task's author can delete it")
    success_url = reverse_lazy("login")
