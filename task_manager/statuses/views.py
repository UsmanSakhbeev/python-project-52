from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.statuses.forms import CustomStatusCreationForm
from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/status_list.html"
    context_object_name = "statuses"
    ordering = ["id"]


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = CustomStatusCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Create Status"), "button_name": _("Create")}
    success_message = _("Status was created successfully")
    success_url = reverse_lazy("status_list")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = CustomStatusCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Update Status"), "button_name": _("Update")}
    success_message = _("Status was updated successfully")
    success_url = reverse_lazy("status_list")


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/status_delete.html"
    extra_context = {"title": _("Delete Status"), "button_name": _("Yes, delete")}
    success_message = _("Status was deleted successfully")
    success_url = reverse_lazy("status_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(
                request,
                _("Cannot delete status because it is associated with existing tasks."),
            )
            return redirect("status_list")
