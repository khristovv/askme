from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver


from .managers import UserManager
from .validators import UsernameValidator
# TODO: add more fields to Profile
# TODO: add version control

# asd1@mail.com - pass: SOMEc00lP@ssW


class User(AbstractUser):
    username_validator = UsernameValidator()
    first_name = None
    last_name = None
    username = models.CharField(
        _("Username for profile page"),
        unique=True,
        max_length=50,
        validators=[username_validator]
    )

    email = models.EmailField(
        _("Email address."),
        unique=True
    )

    is_active = models.BooleanField(
        _("Is user active"),
        default=False
    )
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email} - joined on: {self.date_joined}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # bio = models.TextField(_("Bio to present the user"), default='', blank=True, max_length=250)
    image = models.ImageField(default="default-profile-image.png", upload_to='profile_pics')

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
