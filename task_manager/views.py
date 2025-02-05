from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class LoginView(DjangoLoginView):
    template_name = "login.html"
    next_page = reverse_lazy("index")
    succes_message = _("You were logged in")
    extra_context = {"title": _("Log In"), "button_name": _("Enter")}


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("index")
