from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=150, blank=False, unique=True, verbose_name=_("Name")
    )
    description = models.TextField(blank=False, verbose_name=_("Description"))
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_("Status")
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
        related_name="tasks_created",
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Executor"),
        related_name="tasks_assigned",
    )
    label = models.ManyToManyField(Label, blank=True, verbose_name=_("Label"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
