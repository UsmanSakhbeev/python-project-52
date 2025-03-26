from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelCreationForm
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"
    ordering = ["id"]


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Create Label"), "button_name": _("Create")}
    success_message = _("Label was created successfully")
    success_url = reverse_lazy("label_list")


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Update Label"), "button_name": _("Update")}
    success_message = _("Label was updated successfully")
    success_url = reverse_lazy("label_list")


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/label_delete.html"
    extra_context = {"title": _("Delete Label"), "button_name": _("Yes, delete")}
    success_message = _("Label was deleted successfully")
    success_url = reverse_lazy("label_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Task.objects.filter(label=self.object).exists():
            messages.error(
                request,
                _("Cannot delete label because it is associated with existing tasks."),
            )
            return redirect("label_list")
        return super().post(request, *args, **kwargs)
