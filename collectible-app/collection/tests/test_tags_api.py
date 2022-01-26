from django.contrib.auth import get_user_model as gum
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Tag, Collection
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

    # Tests filtering Tags by those assigned to Collections
    def test_retrieve_tags_assigned_to_collections(self):
        tag1 = Tag.objects.create(user=self.user, name='Favorite')
        tag2 = Tag.objects.create(user=self.user, name='Owned')
        collection = Collection.objects.create(
            title='Mumopins Collection',
            items_in_collection=25,
            floor_price=50.00,
            user=self.user
        )
        collection.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    # Tests that filtering Tags by assigned will return unique items
    def test_retrieve_tags_assigned_unique(self):
        tag = Tag.objects.create(user=self.user, name='Favorite')
        Tag.objects.create(user=self.user, name='Owned')
        collection1 = Collection.objects.create(
            title='Summer Pin Collection',
            items_in_collection=10,
            floor_price=50.00,
            user=self.user,
        )
        collection1.tags.add(tag)
        collection2 = Collection.objects.create(
            title='Fall Pin Collection',
            items_in_collection=12,
            floor_price=50.00,
            user=self.user,
        )
        collection2.tags.add(tag)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
