from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PatronViewSet
from django.contrib.auth import get_user_model

User = get_user_model()

# Test patron view set
class PatronCreateTestCase(APITestCase):
    # Set up function for all the tests for this view
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PatronViewSet.as_view() # This line is a problem
        self.url = reverse('patron')
        self.user = User.objects.create(
            email = 'test@sample.com',
            username = 'testUser',
            user_type = 'patron'
        )


    def patron_test_status(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEquals(response.data['AllergyTag'], {})
        # self.assertEquals(response.data['RestrictionTag'], {})
        # self.assertEquals(response.data['TasteTag'], {})

    def test_patron_creation(self):
        # Create sample patron wihtout any tags
        sample_patron = {
            "name":"Test Patron",
            "dob":"2000-01-01",
            "calorie_limit":600,
            "gender":"male",
            "price_preference": "$$",
            "zipcode":"111110000"
        }

        request = self.factory.post(self.url,sample_patron)
        response = self.view(request) 
        # Tests for the patron created above
        # Test to see if patron is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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