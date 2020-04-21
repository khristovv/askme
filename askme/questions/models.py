from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    asked_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )

    asked_to = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )

    content = models.CharField(
        _("The question"),
        max_length=2048
    )

    created_on = models.DateTimeField(
        _("Date % time the question was asked"),
        default=timezone.now
    )

    updated_on = models.DateTimeField(
        _("Date the question was answered"),
        blank=True
    )