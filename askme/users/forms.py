from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm

from .models import User


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username')


class UserUpdateForm(UserChangeForm):
    pass




