from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
# from .views import PatronViewSet
from django.contrib.auth import get_user_model
from accounts.tokens import create_jwt_pair_for_user
from rest_framework import status
from . import models
#from ..restaurants.models import 

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

        # cls.patron1_user = User.objects.create_user(
        #     email = 'patron1@app.com',
        #     username = 'patron1',
        #     password = 'password',
        #     user_type = 'patron'
        # )
        cls.patron1_user = User.objects.get(email="patron1@app.com")
        cls.patron1_access = create_jwt_pair_for_user(cls.patron1_user)['access']

        # cls.patron2_user = User.objects.create_user(
        #     email = 'patron2@app.com',
        #     username = 'patron2',
        #     password = 'password',
        #     user_type = 'patron'
        # )
        cls.patron2_user = User.objects.get(email="patron2@app.com")
        cls.patron2_access = create_jwt_pair_for_user(cls.patron2_user)['access']

        # cls.restaurant_user = User.objects.create_user(
        #     email = 'restaurant@app.com',
        #     username = 'testRestaurant',
        #     password = 'password',
        #     user_type = 'restaurant'
        # )
        cls.restaurant_user = User.objects.get(email="restaurant@app.com")
        cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

        # cls.admin_user = User.objects.create_user(
        #     email = 'admin@app.com',
        #     username = 'testAdmin',
        #     password = 'password',
        #     user_type = 'admin'
        # )
        cls.admin_user = User.objects.get(email="admin@app.com")
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        #create tags
        # cls.restriction_tag_names = ["Kosher", "Halal", "Vegetarian", "Vegan", "Pescatarian", "Gluten Free"]
        # cls.allergy_tag_names = ["Tree Nut", "Lactose", "Soy", "Egg", "Shellfish", "Gluten"]
        # cls.disliked_ingredient_tags = ["Cheese", "Caramel", "Sardines", "Beef", "Pork", "Celery"]
        # cls.patron_taste_tag_names = ["Fruity", "Savory", "Sweet", "Umami", "Asian Cuisine", "Italian Cuisine"]
        # Lists to store tags in for data input
        # cls.restriction_tags = []
        # cls.allergy_tags = []
        # cls.disliked_ingredients = []
        # cls.patron_taste_tags = []

        # Grab tags for entry in new patrons
        restrict_tag_dict = {tag.title: tag.id for tag in models.RestrictionTag.objects.all()}
        allergy_tag_dict = {tag.title: tag.id for tag in models.AllergyTag.objects.all()}
        disliked_ingredients_dict = {tag.title: tag.id for tag in models.IngredientTag.objects.all()}
        taste_tag_dict = {tag.title: tag.id for tag in models.TasteTag.objects.all()}


        # # Create restriction tags and append them to restriction tag list
        # for tag in cls.restriction_tag_names:
        #     models.RestrictionTag.objects.create(title=tag)
        #     cls.restriction_tags.append(models.RestrictionTag.objects.get(title=tag)) 

        # # Create allergy tags and append them to allergy tag list
        # for tag in cls.allergy_tag_names:
        #     models.AllergyTag.objects.create(title=tag)
        #     cls.allergy_tags.append(models.AllergyTag.objects.get(title=tag)) 

        # # Create disliked ingredient tags and append them to disliked ingredient tag list
        # for tag in cls.disliked_ingredient_tags:
        #     models.IngredientTag.objects.create(title=tag)
        #     cls.disliked_ingredients.append(models.IngredientTag.objects.get(title=tag))

        # # Create taste tags and append them to taste tag list
        # for tag in cls.patron_taste_tag_names:
        #     models.TasteTag.objects.create(title=tag)
        #     cls.patron_taste_tags.append(models.TasteTag.objects.get(title=tag))  

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

        #new data
        # cls.new_data = [
        #     {
        #         "name":"Sue", "dob":"2002-12-12", "calorie_limit":0, "gender":"Female", "price_max":25, "zipcode":23508,
        #         "patron_restriction_tag":[cls.restriction_tags[4].id], "patron_allergy_tag":[cls.allergy_tags[3].id, cls.allergy_tags[4].id],
        #         "disliked_ingredients":[cls.disliked_ingredients[1].id, cls.disliked_ingredients[5].id],
        #         "patron_taste_tag":[cls.patron_taste_tags[2].id, cls.patron_taste_tags[3].id]
        #     },
        #     {
        #         "name":"Doug", "dob":"2003-09-03", "calorie_limit":300, "gender":"Other", "price_max":0, "zipcode":23508,
        #         "patron_restriction_tag":[cls.restriction_tags[2].id], "patron_allergy_tag":[],
        #         "disliked_ingredients":[cls.disliked_ingredients[0], cls.disliked_ingredients[5]], "patron_taste_tag":[cls.patron_taste_tags[5].id]
        #     }
        # ]

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

    # Test if a patron can be created by a patron user
    def test_create_patron_with_patron(self):
        pat0_response = self.client.post(self.list_url, self.data[0], HTTP_AUTHORIZATION=f'Bearer {self.patron0_access}')
        pat1_response = self.client.post(self.list_url, self.data[1], HTTP_AUTHORIZATION=f'Bearer {self.patron1_access}')
        pat2_response = self.client.post(self.list_url, self.data[2], HTTP_AUTHORIZATION=f'Bearer {self.patron2_access}')

        # Patron 0 Tests
        self.assertEqual(pat0_response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(len(pat0_response.data), 24)





    #def test_list_patron(self):
        # patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron0_access}')
        #data = self.new_data[0]
        # print(f'\n{data}\n')
        
        # NOTE: patron 0 already has an associated profile, so it cant send a post request.
        # patron_response = self.client.post(self.list_url, self.new_data[0], HTTP_AUTHORIZATION=f'Bearer {self.patron0_access}')

        # self.assertEqual(patron_response.status_code, status.HTTP_200_OK)

        # profile = models.Patron.objects.filter(user=patron_response.user)
        # self.assertEqual(patron_response.data['name'], profile.name)


#     # def patron_test_status(self):
#     #     request = self.factory.get(self.url)
#     #     response = self.view(request)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     # self.assertEquals(response.data['AllergyTag'], {})
#     #     # self.assertEquals(response.data['RestrictionTag'], {})
#     #     # self.assertEquals(response.data['TasteTag'], {})

#     # def test_patron_creation(self):
#     #     # Create sample patron wihtout any tags
#     #     sample_patron = {
#     #         "name":"Test Patron",
#     #         "dob":"2000-01-01",
#     #         "calorie_limit":600,
#     #         "gender":"male",
#     #         "price_preference": "$$",
#     #         "zipcode":"111110000"
#     #     }

#     #     request = self.factory.post(self.url,sample_patron)
#     #     response = self.view(request) 
#     #     # Tests for the patron created above
#     #     # Test to see if patron is created
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def tearDownClass(cls):
        #models.Patron.objects.all().delete()
        #models.RestrictionTag.objects.all().delete()
        #models.AllergyTag.objects.all().delete()
        #models.IngredientTag.objects.all().delete()
        #models.TasteTag.objects.all().delete()
        User.objects.all().delete()

# # Test patron tags
# # class PatronTagTestCase(APITestCase):
    
# #     def test_tag_overview(self):
# #         response = self.client.get(reverse('analytics'))

# #         # Test status code of view
# #         self.assertEquals(response.status_code, status.HTTP_200_OK)
# #         # Test content of returned response from view
# #         self.assertEquals(response.data['AllergyTag'], {})
# #         self.assertEquals(response.data['RestrictionTag'], {})
# #         self.assertEquals(response.data['TasteTag'], {})
# #         # Can use below code to see what the returned data looks like
# #         #print(response.data)