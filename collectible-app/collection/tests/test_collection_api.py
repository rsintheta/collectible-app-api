import tempfile
import os
from PIL import Image
from django.contrib.auth import get_user_model as gum
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Collection, Tag, Item
from collection.serializers import CollectionSerializer, \
                                   CollectionDetailSerializer

COLLECTIONS_URL = reverse('collection:collection-list')


# Returns a Collection's image URL
def image_upload_url(collection_id):
    return reverse('collection:collection-upload-image', args=[collection_id])


# Returns a Collection's detail URL
def detail_url(collection_id):
    return reverse('collection:collection-detail', args=[collection_id])


# Creates and returns a sample Tag for testing
def sample_tag(user, name='NFTs'):
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


# Tests unauthenticated Collection API features
class PublicCollectionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that authentication is required
    def test_authentication_required(self):
        res = self.client.get(COLLECTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Tests authenticated Collection API features
class PrivateCollectionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = gum().objects.create_user(
            'loremipsum@gmail.com',
            'Tbin5041'
        )
        self.client.force_authenticate(self.user)

    # Tests retrieving a list of Collections
    def test_retrieve_collections(self):
        sample_collection(user=self.user)
        sample_collection(user=self.user)
        res = self.client.get(COLLECTIONS_URL)
        collections = Collection.objects.all().order_by('-id')
        serializer = CollectionSerializer(collections, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Test that a user can only retrieve their own Collections
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

    # Tests viewing a Collections details
    def test_view_collection_detail(self):
        collection = sample_collection(user=self.user)
        collection.tags.add(sample_tag(user=self.user))
        collection.items.add(sample_item(user=self.user))
        url = detail_url(collection.id)
        res = self.client.get(url)
        serializer = CollectionDetailSerializer(collection)
        self.assertEqual(res.data, serializer.data)

    # Tests creating a Collection
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

    # Tests creating a Collection with Tags
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

    # Tests creating a Collection with Items
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

    # Tests updating a Collection with the patch(partial) update
    def test_partial_update_collection(self):
        collection = sample_collection(user=self.user)
        collection.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Pins')
        objectData = {'title': 'Comic-Con 2019 Set', 'tags': [new_tag.id]}
        url = detail_url(collection.id)
        self.client.patch(url, objectData)
        collection.refresh_from_db()
        self.assertEqual(collection.title, objectData['title'])
        tags = collection.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    # Tests updating a Collection with the put(overwrite) update
    def test_full_collection(self):
        collection = sample_collection(user=self.user)
        collection.tags.add(sample_tag(user=self.user))
        objectData = {
            'title': 'Comic-Con 2019 Set',
            'items_in_collection': 10000,
            'floor_price': 50.00,
        }
        url = detail_url(collection.id)
        self.client.put(url, objectData)
        collection.refresh_from_db()
        self.assertEqual(collection.title, objectData['title'])
        self.assertEqual(
            collection.items_in_collection,
            objectData['items_in_collection']
        )
        self.assertEqual(collection.floor_price, objectData['floor_price'])
        tags = collection.tags.all()
        self.assertEqual(len(tags), 0)


# The tests for using the PIL library and uploading images.
class CollectionImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = gum().objects.create_user(
            'loremipsum@gmail.com',
            'Tbin5041'
        )
        self.client.force_authenticate(self.user)
        self.collection = sample_collection(user=self.user)

    def tearDown(self):
        self.collection.image.delete()

    # Tests uploading an image to a Collection
    def test_upload_image_to_collection(self):
        url = image_upload_url(self.collection.id)
        with tempfile.NamedTemporaryFile(suffix='.png') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='PNG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')
        self.collection.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.collection.image.path))

    # Tests that an invalid image cannot be accepted
    def test_upload_image_bad_request(self):
        url = image_upload_url(self.collection.id)
        res = self.client.post(url, {'image': 'error'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests returning Collections with specific Tags
    def test_filtering_collection_by_tags(self):
        collection1 = sample_collection(user=self.user, title='bayc')
        collection2 = sample_collection(
            user=self.user,
            title='Dead Avatar Project'
        )
        tag1 = sample_tag(user=self.user, name='bad')
        tag2 = sample_tag(user=self.user, name='good')
        collection1.tags.add(tag1)
        collection2.tags.add(tag2)
        collection3 = sample_collection(user=self.user, title='comissions')
        res = self.client.get(
            COLLECTIONS_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )
        serializer1 = CollectionSerializer(collection1)
        serializer2 = CollectionSerializer(collection2)
        serializer3 = CollectionSerializer(collection3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    # Tests returning Collections with specific Items
    def test_filter_collection_by_items(self):
        collection1 = sample_collection(user=self.user, title='bayc')
        collection2 = sample_collection(
            user=self.user,
            title='Dead Avatar Project'
            )
        item1 = sample_item(user=self.user, name='boredape111')
        item2 = sample_item(user=self.user, name='DeadAvatar222')
        collection1.items.add(item1)
        collection2.items.add(item2)
        collection3 = sample_collection(user=self.user, title='mumopins')
        res = self.client.get(
            COLLECTIONS_URL,
            {'items': f'{item1.id},{item2.id}'}
        )
        serializer1 = CollectionSerializer(collection1)
        serializer2 = CollectionSerializer(collection2)
        serializer3 = CollectionSerializer(collection3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
