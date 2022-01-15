from django.test import TestCase
from django.contrib.auth import get_user_model as gum
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return gum().objects.create_user(**params)


# Test the public user API
class PublicUserAPITests(TestCase):
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

    # Tests that authentication is required for users
    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Testing the API requests that require authentication first
class PrivateUserAPITests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='loremipsum@gmail.com',
            password='Tbin5041',
            name='Lonestar',
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    # Tests retrieving the profile contained in a user
    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    # Tests that POST is not allowed on the me url.
    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Tests updating the user profile for an authenticated user
    def test_update_user_profile(self):
        userInfo = {
            'name': 'Cody Bentsen',
            'password': 'Tobn2180',
        }
        res = self.client.patch(ME_URL, userInfo)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, userInfo['name'])
        self.assertTrue(self.user.check_password, userInfo['password'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
