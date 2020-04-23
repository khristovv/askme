from django.test import TestCase
from users.models import User

from users.forms import UserCreationForm


class TestUserCreationForm(TestCase):
    def test_bad_username_provided(self):
        form = UserCreationForm(data={
            'email': 'user1@mail.com',
            'username': 'user1/',  # '/' char unsupported
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertFalse(form.is_valid())

    def test_mismatching_passwords(self):
        form = UserCreationForm(data={
            'email': 'user1@mail.com',
            'username': 'user1',
            'password1': 'MISMATCHING_PASSWORDS',
            'password2': 'mismatching_passwords'
        })
        self.assertFalse(form.is_valid())

    def test_user_wil_email_already_exists(self):
        User.objects.create_user('user1@mail.com', 'user1', 'A_VERY-$trong.p@assworD')

        form = UserCreationForm(data={
            'email': 'user1@mail.com',
            'username': 'user1',
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertFalse(form.is_valid())

    def test_valid_form_scenario(self):
        form = UserCreationForm(data={
            'email': 'email2@mail.com',
            'username': 'bad-username',
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertTrue(form.is_valid())


