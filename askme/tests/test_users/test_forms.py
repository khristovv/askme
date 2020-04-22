from django.test import TestCase

from users.forms import UserCreationForm


class TestForms(TestCase):
    def test_UserCreationForm_is_invalid(self):
        form = UserCreationForm(data={
            'email': 'email1@mail.com',
            'username': 'bad-username/',  # '/' char unsupported
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertFalse(form.is_valid())

        form = UserCreationForm(data={
            'email': 'email1@mail.com',
            'username': 'bad-username',
            'password1': 'MISMATCHING_PASSWORDS',
            'password2': 'mismatching_passwords'
        })
        self.assertFalse(form.is_valid())

    def test_UserCreationForm_is_valid(self):
        form = UserCreationForm(data={
            'email': 'email2@mail.com',
            'username': 'bad-username',
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertTrue(form.is_valid())


