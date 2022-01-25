from django.contrib.auth import get_user_model as gum
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Item
from collection.serializers import ItemSerializer


ITEMS_URL = reverse('collection:item-list')


# Test the publicly available functions of the Items API
class PublicItemsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Tests that only Users can access the Items endpoint
    def test_login_required(self):
        res = self.client.get(ITEMS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Tests the features of the Items API that require authentication
class PrivateItemsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = gum().objects.create_user(
            'loremipsum@gmail.com',
            'Tbin5041'
        )
        self.client.force_authenticate(self.user)

    # Tests retrieving a list of Items
    def test_retrieve_item_list(self):
        Item.objects.create(user=self.user, name='Monster')
        Item.objects.create(user=self.user, name='DeadAvatar400')
        res = self.client.get(ITEMS_URL)
        items = Item.objects.all().order_by('-name')
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Tests that only the Items for the authenticated User are returned
    def test_items_limited_to_user(self):
        user2 = gum().objects.create_user(
            'oremlipsum@gmail.com',
            'Tobn2180'
        )
        Item.objects.create(user=user2, name='DeadAvatar369')
        item = Item.objects.create(user=self.user, name='DeadAvatar867')
        res = self.client.get(ITEMS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], item.name)

    # Tests the successful creation of an Item
    def test_create_item_successful(self):
        item = {'name': 'Cowboy'}
        self.client.post(ITEMS_URL, item)
        exists = Item.objects.filter(
            user=self.user,
            name=item['name']
        ).exists()
        self.assertTrue(exists)

    # Tests creating an Item with invalid information
    def test_create_item_invalid(self):
        item = {'name': ''}
        res = self.client.post(ITEMS_URL, item)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
