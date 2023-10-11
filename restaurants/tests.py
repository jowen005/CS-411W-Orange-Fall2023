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



    def test_list(self):
        """Ensure we can list out existing rest tags"""
        expected = ['Mexican', 'Fast Food', 'Bar']

        response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        for tag in expected:
            self.assertTrue(models.RestTag.objects.filter(title=tag).exists())

    def test_create(self):
        """Ensure only admin can can create a rest tag"""
        data = {"title":"Thai"}

        response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(models.RestTag.objects.all()), 4)
        self.assertTrue(models.RestTag.objects.filter(title=data['title']).exists())


    @classmethod
    def tearDownClass(cls):
        models.RestTag.objects.all().delete()
        User.objects.all().delete()