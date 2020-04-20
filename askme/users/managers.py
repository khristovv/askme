from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, **kwargs):
        """
        Should accept the USERNAME field and all required fields to create a new user.
        :return: a newly created user
        """
        if not email:
            raise ValueError(_('Must provide a valid email address!'))

        if not username:
            raise ValueError(_('A username must be provided!'))

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_staff = kwargs.get('is_staff', False)
        user.is_superuser = kwargs.get('is_superuser', False)
        user.is_active = kwargs.get('is_active', False)
        user.save()
        return user

    def create_user(self, email, username, password):
        return self._create_user(
            email, username, password
        )

    def create_superuser(self, email, username, password):
        return self._create_user(
            email, username, password, is_staff=True, is_superuser=True, is_active=True
        )
