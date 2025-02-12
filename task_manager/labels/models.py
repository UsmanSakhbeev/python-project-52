from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    """
    def delete(self, *args, **kwargs):
        if self.tasks.exists:
            error_message = _("Cannot delete this label because it is being used")
            raise ProtectedError(error_message, self.tasks.all)
        return super().delete(*args, **kwargs)
    """
