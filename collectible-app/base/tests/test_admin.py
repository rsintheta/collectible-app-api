from django.test import TestCase, Client
from django.contrib.auth import get_user_model as gum
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = gum().objects.create_superuser(
            email='loremipsum@gmail.com',
            password='Tbin5041',
            )
        self.client.force_login(self.admin_user)
        self.user = gum().objects.create_user(
            email='lomeripmus@gmail.com',
            password='Tbin1504',
            name='Lorem Ipsum',
            )

    # Tests that the Users are properly listed on the User page
    def test_users_listed(self):
        url = reverse('admin:base_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    # Tests the edit User page
    def test_user_change_page(self):
        url = reverse('admin:base_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    # Tests the create User page
    def test_create_user_page(self):
        url = reverse('admin:base_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
