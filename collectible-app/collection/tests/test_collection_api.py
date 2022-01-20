from django.contrib.auth import get_user_model as gum
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Collection
from collection.serializers import CollectionSerializer

COLLECTIONS_URL = reverse('collection:collection-list')


# Creates and returns a sample collection
def sample_collection(user, **params):
    defaults = {
        'title': 'Dead Avatar Project',
        'items_in_collection': 10000,
        'floor_price': 0.50,
    }
    defaults.update(params)
    return Collection.objects.create(user=user, **defaults)


# Tests unauthenticated collection API access
class PublicCollectionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that authentication is required
    def test_authentication_required(self):
        res = self.client.get(COLLECTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Tests authenticated collection API access
class PrivateCollectionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = gum().objects.create_user(
            'loremipsum@gmail.com',
            'Tbin5041'
        )
        self.client.force_authenticate(self.user)

    # Tests retrieving a list of collections
    def test_retrieve_collections(self):
        sample_collection(user=self.user)
        sample_collection(user=self.user)
        res = self.client.get(COLLECTIONS_URL)
        collections = Collection.objects.all().order_by('-id')
        serializer = CollectionSerializer(collections, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Test that retrieves collections for user
    def test_collections_limited_to_user(self):
        user2 = gum().objects.create_user(
            'oremlipsum@gmail.com',
            'Tbin5041'
        )
        sample_collection(user=user2)
        sample_collection(user=self.user)
        res = self.client.get(COLLECTIONS_URL)
        collections = Collection.objects.filter(user=self.user)
        serializer = CollectionSerializer(collections, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
