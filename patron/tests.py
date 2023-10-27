from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PatronViewSet
from django.contrib.auth import get_user_model
from accounts.tokens import create_jwt_pair_for_user
from rest_framework import status
from . import models

User = get_user_model()

# Test patron view set
class PatronCreateTestCase(APITestCase):
    # Set up function for all the tests for this view
    @classmethod
    def setUpClass(cls):
        # self.factory = APIRequestFactory()
        # self.view = PatronViewSet.as_view() # This line is a problem

        # Create users and access tokens
        cls.patron0 = User.objects.create(
            email = 'test@sample.com',
            username = 'testUser',
            user_type = 'patron'
        )
        cls.patron0_access = create_jwt_pair_for_user(cls.patron0)['access']

        cls.new_patron = User.objects.create(
            email = 'newuser@sample.com',
            username = 'newUser',
            user_type = 'patron'
        )
        cls.patron0_access = create_jwt_pair_for_user(cls.patron0)['access']

        #create tags

        
        #create data objects to instantiate
        cls.data = [
            {
                'user':cls.patron0, 
            }
        ]

        #new data
        cls.new_data = [
            {
                'user':1
            }
        ]

        #Url Stuff
        cls.basename = 'patron'
        cls.list_url = reverse(f'{cls.basename}-list') #list and create (get, post)
          
        cls.detail_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 1})
        cls.invalid_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 10}) #retrieve, update, delete

        # cls.url = reverse('patron')


    def test_list_patron(self):
        patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron0_access}')
        patron_response = self.client.post(self.list_url, self.data, HTTP_AUTHORIZATION=f'Bearer {self.patron0_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_200_OK)

        profile = models.Patron.objects.filter(user=patron_response.user)
        self.assertEqual(patron_response.data['name'], profile.name)


    # def patron_test_status(self):
    #     request = self.factory.get(self.url)
    #     response = self.view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEquals(response.data['AllergyTag'], {})
    #     # self.assertEquals(response.data['RestrictionTag'], {})
    #     # self.assertEquals(response.data['TasteTag'], {})

    # def test_patron_creation(self):
    #     # Create sample patron wihtout any tags
    #     sample_patron = {
    #         "name":"Test Patron",
    #         "dob":"2000-01-01",
    #         "calorie_limit":600,
    #         "gender":"male",
    #         "price_preference": "$$",
    #         "zipcode":"111110000"
    #     }

    #     request = self.factory.post(self.url,sample_patron)
    #     response = self.view(request) 
    #     # Tests for the patron created above
    #     # Test to see if patron is created
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def tearDownClass(self):
        User.objects.all().delete()

# Test patron tags
# class PatronTagTestCase(APITestCase):
    
#     def test_tag_overview(self):
#         response = self.client.get(reverse('analytics'))

#         # Test status code of view
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         # Test content of returned response from view
#         self.assertEquals(response.data['AllergyTag'], {})
#         self.assertEquals(response.data['RestrictionTag'], {})
#         self.assertEquals(response.data['TasteTag'], {})
#         # Can use below code to see what the returned data looks like
#         #print(response.data)