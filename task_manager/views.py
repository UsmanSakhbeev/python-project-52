from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class LoginView(SuccessMessageMixin, DjangoLoginView):
    template_name = "form.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("index")
    succes_message = _("You were logged in")
    extra_context = {"title": _("Log In"), "button_name": _("Enter")}


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _("You were logged out"))
        return super().dispatch(request, *args, **kwargs)
