from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class UserPermissionMixin(UserPassesTestMixin):
    permission_denied_message = _("You don't have rights to change another user.")

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect("user_list")


class TaskAuthorPermissionMixin(UserPassesTestMixin):
    permission_denied_message = _("Only the task's author can delete it")
    raise_exception = False

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse_lazy("task_list"))
