from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    # Test creating users
    def test_create_user_with_email_successful(self):
        email = 'loremipsum@gmail.com'
        password = 'Tbin5041'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # Test that the email is normalized
    def test_new_user_email_normalized(self):
        email = 'loremipsum@GMail.cOM'
        user = get_user_model().objects.create_user(email, 'Tbin5041')
        self.assertEqual(user.email, email.lower())

    # Test to make sure entered email is valid
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'tobn')

    # Test creating a superuser
    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser('mloremipsu@gmail.com', 'Tbin5041')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
