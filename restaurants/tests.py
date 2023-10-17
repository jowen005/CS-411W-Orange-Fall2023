from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from . import models
from django.contrib.auth import get_user_model
from accounts.tokens import create_jwt_pair_for_user

User = get_user_model()

# Create your tests here.
class RestTagTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        models.RestTag.objects.create(title='Mexican')
        models.RestTag.objects.create(title='Fast Food')
        models.RestTag.objects.create(title='Bar')

        cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
                            username='admin', password="password", user_type='admin')
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
                            username='restaurant', password="password", user_type='restaurant')
        cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

        cls.patron_user = User.objects.create_user(email="patron@app.com", 
                            username='patron', password="password", user_type='patron')
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

        cls.list_url = reverse('resttags-list')
        cls.detail_url = reverse('resttags-detail', kwargs={'pk': 1})
        cls.invalid_url = reverse('resttags-detail', kwargs={'pk': 10})

    def test_list_tag_allusers(self):
        """Ensure all users can list out existing rest tags"""
        expected = ['Mexican', 'Fast Food', 'Bar']

        admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(admin_response.data), 3)

        self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(patron_response.data), 3)
        
        self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rest_response.data), 3)
        
    def test_create_tag_admin(self):
        """Ensure admin can create a rest tag"""
        data = {"title":"Thai"}

        admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
        self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(models.RestTag.objects.all()), 4)
        self.assertTrue(models.RestTag.objects.filter(title=data['title']).exists())

    def test_create_tag_nonadmin(self):
        """Ensure nonadmin can not create a rest tag"""
        data = {"title":"Mongolian"}

        patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(models.RestTag.objects.all()), 3)
        self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

        self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(models.RestTag.objects.all()), 3)
        self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

    def test_retrieve_tag_allusers(self):
        """Ensure all users can retrieve a rest tag"""

        admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
        invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data["title"], models.RestTag.objects.get(id=admin_response.data["id"]).title)

        self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patron_response.data["title"], models.RestTag.objects.get(id=patron_response.data["id"]).title)

        self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
        self.assertEqual(rest_response.data["title"], models.RestTag.objects.get(id=rest_response.data["id"]).title)

        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tag_admin(self):
        """Ensure admin can retrieve a rest tag"""
        data = {"title":"Thai"}

        admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data["title"], data["title"])
        self.assertEqual(models.RestTag.objects.get(id=admin_response.data["id"]).title, data["title"])

        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tag_nonadmin(self):
        """Ensure nonadmin can not retrieve a rest tag"""
        data = {"title":"Mongolian"}

        patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

        self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

    def test_delete_tag_admin(self):
        """Ensure admin can delete a rest tag"""
        response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        deleted_data = response.data["title"]

        admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(models.RestTag.objects.all()), 2)
        self.assertFalse(models.RestTag.objects.filter(title=deleted_data).exists())

        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_tag_nonadmin(self):
        """Ensure nonadmin can not delete a rest tag"""
        patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def tearDownClass(cls):
        models.RestTag.objects.all().delete()
        User.objects.all().delete()