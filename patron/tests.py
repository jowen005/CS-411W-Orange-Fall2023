from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
# Test patron view set

# Test patron tags
class PatronTagTestCase(APITestCase):
    
    def test_tag_overview(self):
        response = self.client.get(reverse('analytics'))

        self.assertEquals(response.status_code, status.HTTP_200_OK)