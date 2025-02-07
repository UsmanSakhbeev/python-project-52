from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
