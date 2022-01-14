from django.test import TestCase
from django.contrib.auth import get_user_model as gum
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return gum().objects.create_user(**params)


# Test the public user API
class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Test creating a user with valid credentials is successful
    def test_create_valid_user_success(self):
        userInfo = {
            'email': 'loremipsum@gmail.com',
            'password': 'TBN514',
            'name': 'Lonestar',
        }
        res = self.client.post(CREATE_USER_URL, userInfo)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = gum().objects.get(**res.data)
        self.assertTrue(user.check_password(userInfo['password']))
        self.assertNotIn('password', res.data)

    # Test trying to create a user that already exists in the database
    def test_user_exists(self):
        userInfo = {
            'email': 'loremipsum@gmail.com',
            'password': 'TBN514',
            'name': 'Lonestar',
            }
        create_user(**userInfo)

        res = self.client.post(CREATE_USER_URL, userInfo)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test that the password has enough characters
    def test_password_too_short(self):
        userInfo = {
            'email': 'loremipsum@gmail.com',
            'password': 'TBN',
            'name': 'Lonestar',
            }
        res = self.client.post(CREATE_USER_URL, userInfo)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = gum().objects.filter(
            email=userInfo['email']
        ).exists()
        self.assertFalse(user_exists)

    # Tests that a token is successfully created for the user
    def test_create_token_for_user(self):
        userInfo = {
            'email': 'loremipsum@gmail.com',
            'password': 'TBN',
            'name': 'Lonestar',
            }
        create_user(**userInfo)
        res = self.client.post(TOKEN_URL, userInfo)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Tests that tokens are not created if credentials are not valid
    def test_create_token_invalid_credentials(self):
        create_user(email='loremipsum@gmail.com', password='TBN514',
                    name='Lonestar')
        badCredentials = {'email': 'loremipsum@gmail.com', 'password': 'RGGE'}
        res = self.client.post(TOKEN_URL, badCredentials)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Make sure if there is no user, no token is granted
    def test_create_token_no_user(self):
        userInfo = {
            'email': 'loremipsum@gmail.com',
            'password': 'TBN',
            'name': 'Lonestar',
            }
        res = self.client.post(TOKEN_URL, userInfo)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests that the email and password are required for a token
    def test_create_token_missing_field(self):
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
