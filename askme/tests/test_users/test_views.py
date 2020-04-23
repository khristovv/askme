from django.core import mail
from django.test import TestCase
from django.shortcuts import reverse

from users.models import User


class TestRegisterView(TestCase):
    def test_successful_registration_process(self):
        response = self.client.post(reverse('register'), {
            'email': 'user1@mail.com',
            'username': 'user1',
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Account Confirmation')
        self.assertEqual(mail.outbox[0].recipients(), ['user1@mail.com'])

        created_user = User.objects.get(email='user1@mail.com')
        self.assertEqual(created_user.email, 'user1@mail.com')
        self.assertEqual(created_user.username, 'user1')
        self.assertEqual(created_user.is_active, False)
        self.assertEqual(created_user.is_staff, False)

    def test_when_existing_email_is_given_dont_register_user(self):
        User.objects.create_user(
            'user1@mail.com',
            'user1',
            'A_VERY-$trong.p@assworD'
        )
        response = self.client.post(reverse('register'), {
            'email': 'user1@mail.com',
            'username': 'user1',
            'password1': 'A_VERY-$trong.p@assworD',
            'password2': 'A_VERY-$trong.p@assworD'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(mail.outbox), 0)
