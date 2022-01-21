from django.contrib.auth import get_user_model as gum
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Collection, Tag, Item
from collection.serializers import CollectionSerializer, \
                                   CollectionDetailSerializer

COLLECTIONS_URL = reverse('collection:collection-list')


# Returns collection detail URL
def detail_url(collection_id):
    return reverse('collection:collection-detail', args=[collection_id])


# Creates and returns a sample Tag for testing
def sample_tag(user, name='Pins'):
    return Tag.objects.create(user=user, name=name)


# Creates and returns a sample Item for testing
def sample_item(user, name='DeadAvatar001'):
    return Item.objects.create(user=user, name=name)


# Creates and returns a sample Collection for testing
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

    # Tests viewing a collection detail
    def test_view_collection_detail(self):
        collection = sample_collection(user=self.user)
        collection.tags.add(sample_tag(user=self.user))
        collection.items.add(sample_item(user=self.user))
        url = detail_url(collection.id)
        res = self.client.get(url)
        serializer = CollectionDetailSerializer(collection)
        self.assertEqual(res.data, serializer.data)

    # Tests creating a collection
    def test_create_basic_collection(self):
        collection = {
            'title': 'Dead Avatar Project',
            'items_in_collection': 10000,
            'floor_price': 0.50,
        }
        res = self.client.post(COLLECTIONS_URL, collection)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        collectionID = Collection.objects.get(id=res.data['id'])
        for key in collection.keys():
            self.assertEqual(collection[key], getattr(collectionID, key))

    # Tests creating a collection with tags
    def test_create_collection_with_tags(self):
        tag1 = sample_tag(user=self.user, name='Pins')
        tag2 = sample_tag(user=self.user, name='NFTs')
        collection = {
            'title': 'Dead Avatar Project',
            'tags': [tag1.id, tag2.id],
            'items_in_collection': 10000,
            'floor_price': 0.50,
        }
        res = self.client.post(COLLECTIONS_URL, collection)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        collectionID = Collection.objects.get(id=res.data['id'])
        tags = collectionID.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    # Tests creating a collection with items
    def test_create_collection_with_items(self):
        item1 = sample_item(user=self.user, name='DeadAvatar456')
        item2 = sample_item(user=self.user, name='DeadAvatar001')
        collection = {
            'title': 'Dead Avatar Project',
            'items': [item1.id, item2.id],
            'items_in_collection': 10000,
            'floor_price': 0.50,
        }
        res = self.client.post(COLLECTIONS_URL, collection)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        collectionID = Collection.objects.get(id=res.data['id'])
        items = collectionID.items.all()
        self.assertEqual(items.count(), 2)
        self.assertIn(item1, items)
        self.assertIn(item2, items)
