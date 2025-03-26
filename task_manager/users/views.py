from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import UserPermissionMixin
from task_manager.users.forms import CustomUserChangeForm, CustomUserCreationForm
from task_manager.users.models import User


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    ordering = ["id"]


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "form.html"
    extra_context = {"title": _("Registration"), "button_name": _("Register")}
    success_message = _("User was registrated succesfully")
    success_url = reverse_lazy("login")


class UserUpdateView(
    SuccessMessageMixin, UserPermissionMixin, UpdateView, LoginRequiredMixin
):
    model = User
    form_class = CustomUserChangeForm
    template_name = "form.html"
    extra_context = {"title": _("Update User"), "button_name": _("Update")}
    success_message = _("User was updated succesfully")
    success_url = reverse_lazy("user_list")


class UserDeleteView(
    SuccessMessageMixin, UserPermissionMixin, DeleteView, LoginRequiredMixin
):
    model = User
    template_name = "users/user_delete.html"
    extra_context = {"title": _("Delete user"), "button_name": _("YesDelete")}
    success_message = _("User was deleted succesfully")
    success_url = reverse_lazy("login")
