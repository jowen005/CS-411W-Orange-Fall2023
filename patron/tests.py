from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PatronViewSet

# Test patron view set
class PatronCreateTestCase(APITestCase):
    # Set up function for all the tests for this view
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PatronViewSet.as_view()
        self.url = reverse('patron')


    def idk(self):
        request = self.factory.get(self.url)
        response = self.view(request)

# Test patron tags
class PatronTagTestCase(APITestCase):
    
    def test_tag_overview(self):
        response = self.client.get(reverse('analytics'))

        # Test status code of view
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Test content of returned response from view
        self.assertEquals(response.data['AllergyTag'], {})
        self.assertEquals(response.data['RestrictionTag'], {})
        self.assertEquals(response.data['TasteTag'], {})
        # Can use below code to see what the returned data looks like
        #print(response.data)