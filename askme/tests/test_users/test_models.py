from django.test import TestCase
from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('user1@mail.com', 'user1', 'password')
        User.objects.create_superuser('user2@mail.com', 'user2', 'password')

    def test_normal_user_is_not_active_and_is_not_staff(self):
        user1 = User.objects.get(email='user1@mail.com')
        self.assertFalse(user1.is_staff)
        self.assertFalse(user1.is_active)

    def test_admin_user_is_active_and_is_staff(self):
        user2 = User.objects.get(email='user2@mail.com')
        self.assertTrue(user2.is_staff, True)
        self.assertTrue(user2.is_active, True)
