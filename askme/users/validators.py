import re

from django.core import validators
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UsernameValidator(validators.RegexValidator):
    MIN_USERNAME_LENGTH = 3
    regex = f'^{settings.USERNAME_REGEX_PATTERN}$'
    message = _(
        "A valid username consists of English letters (lower and upper case), "
        "numbers, and the following characters: '.', '_', '-'"
    )
    flags = re.ASCII

    def _validate_min_length(self, value):
        if len(value) < self.MIN_USERNAME_LENGTH:
            raise ValidationError(_("Username must have more than 2 characters!"))

    def __call__(self, value):
        self._validate_min_length(value)
        super().__call__(value)
