from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from . import models
from accounts.tokens import create_jwt_pair_for_user


User = get_user_model()

# Test patron view set
class PatronTests(APITestCase):
    # Import fixtures for this set of tests
    fixtures = ['users.json', 'menuitemtags.json']
    # Set up function for all the tests for this view
    @classmethod
    def setUpClass(cls):
        super().setUpClass() # Calls fixtures before setting up class

        # Create users and access tokens
        cls.patron0_user = User.objects.get(email="patron0@app.com")
        cls.patron0_access = create_jwt_pair_for_user(cls.patron0_user)['access']

        cls.patron1_user = User.objects.get(email="patron1@app.com")
        cls.patron1_access = create_jwt_pair_for_user(cls.patron1_user)['access']

        cls.patron2_user = User.objects.get(email="patron2@app.com")
        cls.patron2_access = create_jwt_pair_for_user(cls.patron2_user)['access']

        cls.restaurant_user = User.objects.get(email="restaurant@app.com")
        cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

        cls.admin_user = User.objects.get(email="admin@app.com")
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        # Grab tags for entry in new patrons
        restrict_tag_dict = {tag.title: tag.id for tag in models.RestrictionTag.objects.all()}
        allergy_tag_dict = {tag.title: tag.id for tag in models.AllergyTag.objects.all()}
        disliked_ingredients_dict = {tag.title: tag.id for tag in models.IngredientTag.objects.all()}
        taste_tag_dict = {tag.title: tag.id for tag in models.TasteTag.objects.all()}

        #create data objects to instantiate
        cls.data = [
            {
                "user":cls.patron0_user, "name":"Stan", "dob":"2003-07-10", "calorie_limit": 3000, "gender":"Male",
                "price_max":20, "zipcode":23508, "patron_restriction_tag":[restrict_tag_dict['Kosher']], "patron_allergy_tag":[allergy_tag_dict['Soy']],
                "disliked_ingredients":[disliked_ingredients_dict['Lettuce']], "patron_taste_tag":[taste_tag_dict['Fruity'], taste_tag_dict['Savory']]
            },
            {
                "user":cls.patron1_user, "name":"Max", "dob":"2004-06-15", "calorie_limit": 450, "gender": "Male", 
                "price_max":30, "zipcode":23508, "patron_restriction_tag":[restrict_tag_dict['Halal'], restrict_tag_dict['Vegan'], restrict_tag_dict['Gluten Free']],
                "patron_allergy_tag":[allergy_tag_dict['Gluten'], allergy_tag_dict['Tree Nut'], allergy_tag_dict['Lactose']],
                "disliked_ingredients":[disliked_ingredients_dict['Caramel'], disliked_ingredients_dict['Beef']],
                "patron_taste_tag":[taste_tag_dict['Sweet'], taste_tag_dict['Savory'], taste_tag_dict['Salty']]
            },
            {
                "user":cls.patron2_user, "name":"Jessie", "dob":"2002-10-06", "calorie_limit": 1000, "gender":"Female",
                "price_max":50, "zipcode":23508, "patron_restriction_tag":[], "patron_allergy_tag":[], "disliked_ingredients":[],
                "patron_taste_tag":[]
            }
        ]

        # Create the tags
        for obj in cls.data:
            patron_restriction_tags = obj.pop('patron_restriction_tag')
            patron_allergy_tags = obj.pop('patron_allergy_tag')
            disliked_ingredients_tags = obj.pop('disliked_ingredients')
            patron_taste_tags = obj.pop('patron_taste_tag')
            instance = models.Patron.objects.create(**obj)
            instance.patron_restriction_tag.set(patron_restriction_tags)
            instance.patron_allergy_tag.set(patron_allergy_tags)
            instance.disliked_ingredients.set(disliked_ingredients_tags)
            instance.patron_taste_tag.set(patron_taste_tags)

        #Url Access
        cls.basename = 'patron'
        cls.list_url = reverse(f'{cls.basename}-list') # list and create (get, post)
          
        cls.detail_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 1})
        cls.invalid_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 10}) #retrieve, update, delete

    # Test if patron user accounts can access their patron profiles
    def test_list_patron_with_patron(self):
        pat0_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron0_access}')
        pat1_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron1_access}')
        pat2_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron2_access}')

        #Pat0 Tests
        self.assertEqual(pat0_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(pat0_response.data), 1)

        pat_owned = list(models.Patron.objects.filter(user=self.patron0_user).values_list('id',flat=True))
        for obj in pat0_response.data:
            self.assertTrue(obj["id"] in pat_owned)
            pat_owned.remove(obj["id"])

        self.assertEqual(len(pat_owned), 0)

        #Pat1 Tests
        self.assertEqual(pat1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(pat1_response.data), 1)

        pat_owned = list(models.Patron.objects.filter(user=self.patron1_user).values_list('id',flat=True))
        for obj in pat1_response.data:
            self.assertTrue(obj["id"] in pat_owned)
            pat_owned.remove(obj["id"])

        self.assertEqual(len(pat_owned), 0)

        #Pat2 Tests
        self.assertEqual(pat2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(pat2_response.data), 1)

        pat_owned = list(models.Patron.objects.filter(user=self.patron2_user).values_list('id',flat=True))
        for obj in pat2_response.data:
            self.assertTrue(obj["id"] in pat_owned)
            pat_owned.remove(obj["id"])

        self.assertEqual(len(pat_owned), 0)

    # Test if admin and restaurant users cannot access patron accounts
    def test_list_patron_with_other_user(self):
        admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        restaurant_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        # Admin test
        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        # Restaurant test
        self.assertEqual(restaurant_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(restaurant_response.data["detail"], "You do not have permission to perform this action.")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
