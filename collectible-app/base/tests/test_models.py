from django.test import TestCase
from django.contrib.auth import get_user_model as gum
from base import models


# Helper function to create users for tests
def sample_user(email='loremipsum@gmail.com', password='Tbin5041'):
    return gum().objects.create_user(email, password)


class ModelTests(TestCase):
    # Test creating users
    def test_create_user_with_email_successful(self):
        email = 'loremipsum@gmail.com'
        password = 'Tbin5041'
        user = gum().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # Test that the email is normalized
    def test_new_user_email_normalized(self):
        email = 'loremipsum@GMail.cOM'
        user = gum().objects.create_user(email, 'Tbin5041')
        self.assertEqual(user.email, email.lower())

    # Test to make sure entered email is valid
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            gum().objects.create_user(None, 'tobn')

    # Test creating a superuser
    def test_create_new_superuser(self):
        user = gum().objects.create_superuser(
            'mloremipsu@gmail.com', 'Tbin5041')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # Tests the tag string representation
    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Autumn Pin Collection'
        )
        self.assertEqual(str(tag), tag.name)
