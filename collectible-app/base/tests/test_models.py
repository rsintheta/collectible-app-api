from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model as gum
from base import models


# Helper function that creates users for tests
def sample_user(email='loremipsum@gmail.com', password='Tbin5041'):
    return gum().objects.create_user(email, password)


class ModelTests(TestCase):
    # Tests creating Users
    def test_create_user_with_email_successful(self):
        email = 'loremipsum@gmail.com'
        password = 'Tbin5041'
        user = gum().objects.create_user(
            email=email,
            password=password,
            )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # Tests that the email is normalized, otherwise the end is case sensitive
    def test_new_user_email_normalized(self):
        email = 'loremipsum@GMail.cOM'
        user = gum().objects.create_user(email, 'Tbin5041')
        self.assertEqual(user.email, email.lower())

    # Tests to make sure the entered email is valid input
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            gum().objects.create_user(None, 'tobn')

    # Tests creating a new Superuser
    def test_create_new_superuser(self):
        user = gum().objects.create_superuser(
            'mloremipsu@gmail.com',
            'Tbin5041',
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # Tests the Tag string representation
    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Autumn Pin Collection',
        )
        self.assertEqual(str(tag), tag.name)

    # Tests the Item string representation
    def test_item_str(self):
        item = models.Item.objects.create(
            user=sample_user(),
            name='Monster',
        )

        self.assertEqual(str(item), item.name)

    # Tests the Collection string representation
    def test_collection_str(self):
        collection = models.Collection.objects.create(
            user=sample_user(),
            title='Dead Avatar Project',
            items_in_collection=10000,
            floor_price=0.50,
        )
        self.assertEqual(str(collection), collection.title)

    # Mock Decorator that creates a uuid4 we would expect from a valid image.
    @patch('uuid.uuid4')
    # Tests that images are saved to the current location
    def test_collection_filename_uuid(self, mock_uuid):
        uuid = 'foo-uuid'
        mock_uuid.return_value = uuid
        file_path = models.collection_image_file_path(None, 'testImage.png')
        expected_path = f'uploads/collection/{uuid}.png'
        self.assertEqual(file_path, expected_path)
