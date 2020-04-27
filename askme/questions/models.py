from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    asked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions_posted',
        blank=True,
        null=True
    )

    asked_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions_received'
    )

    content = models.CharField(
        _("The question"),
        max_length=512
    )

    asked_on = models.DateTimeField(
        _("Date & time the question was created"),
        default=timezone.now,
        blank=True
    )

    hidden = models.BooleanField(
        _("Hide question from user's profile page"),
        blank=True,
        default=False
    )

    def __str__(self):
        return f"Asked by {self.asked_by} to {self.asked_to} on {self.asked_on}"


class Answer(models.Model):
    question = models.OneToOneField(
        'questions.Question',
        on_delete=models.CASCADE,
        related_name='answer'
    )

    answered_on = models.DateTimeField(
        _("Date & time the answer was created"),
        blank=True,
        default=timezone.now
    )

    content = models.CharField(
        _('The answer'),
        max_length=1024
    )

    def __str__(self):
        return f"Question {self.question} answered on {self.answered_on}"


class Like(models.Model):
    answer = models.ForeignKey(
        'questions.Answer',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='liked_answers'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'answer', 'user'
                ],
                name='user_liked'
            )
        ]

    def __str__(self):
        return f"Answer {self.answer} liked by {self.user}"

