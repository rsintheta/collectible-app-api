from django.contrib.auth import get_user_model as gum
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Tag
from collection.serializers import TagSerializer


TAGS_URL = reverse('collection:tag-list')


# Test the publicly available features of the Tags in the API
class PublicTagsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Make sure you can't retrieve Tags without authentication
    def test_login_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Tests the Tags features in the API that require authentication
class PrivateTagsAPITests(TestCase):
    def setUp(self):
        self.user = gum().objects.create_user(
            'loremipsum@gmail.com',
            'Tbin5041')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # Tests retrieving User Tags
    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Pins')
        Tag.objects.create(user=self.user, name='bayc')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Tests that the Tags returned are for the authenticated User
    def test_tags_limited_to_user(self):
        user2 = gum().objects.create_user('oremlipsum@gmail.com', 'Tobn2180')
        Tag.objects.create(user=user2, name='DAP')
        tag = Tag.objects.create(user=self.user, name='Warhammer')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    # Tests creation of a new Tag
    def test_create_tag_successful(self):
        tag = {'name': 'Pins'}
        self.client.post(TAGS_URL, tag)

        exists = Tag.objects.filter(
            user=self.user,
            name=tag['name']
        ).exists()
        self.assertTrue(exists)

    # Tests creating a Tag with invalid data
    def test_create_tag_invalid(self):
        tag = {'name': ''}
        res = self.client.post(TAGS_URL, tag)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
