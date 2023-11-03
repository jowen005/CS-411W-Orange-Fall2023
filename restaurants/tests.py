from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from . import models
from django.contrib.auth import get_user_model
from accounts.tokens import create_jwt_pair_for_user
from abc import ABC

User = get_user_model()


class MenuItemTests(APITestCase):
    fixtures = ['users.json', 
                'resttags.json', 
                'restaurants.json', 
                'menuitemtags.json', 
                'menuitems.json'
                ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.restaurant0_user = User.objects.get(email="restaurant0@app.com")
        cls.restaurant0_access = create_jwt_pair_for_user(cls.restaurant0_user)['access']

        cls.restaurant1_user = User.objects.get(email="restaurant1@app.com")
        cls.restaurant1_access = create_jwt_pair_for_user(cls.restaurant1_user)['access']
        
        cls.admin_user = User.objects.get(email="admin@app.com")
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        cls.patron_user = User.objects.get(email="patron@app.com")
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

        cls.rest_dict = {rest.name: rest.id  for rest in models.Restaurant.objects.all()}

        # Grab tags for entry into new_menuitems {"title": "id"}
        food_tag_dict = {tag.title: tag.id for tag in models.FoodTypeTag.objects.all()}
        cook_tag_dict = {tag.title: tag.id for tag in models.CookStyleTag.objects.all()}
        taste_tag_dict = {tag.title: tag.id for tag in models.TasteTag.objects.all()}
        restrict_tag_dict = {tag.title: tag.id for tag in models.RestrictionTag.objects.all()}
        allergy_tag_dict = {tag.title: tag.id for tag in models.AllergyTag.objects.all()}
        ingred_tag_dict = {tag.title: tag.id for tag in models.IngredientTag.objects.all()}

        cls.new_menuitems = [
            {
                "item_name": "New MI 0", "average_rating": 2.8, "price": 9.99, "calories": 200, 
                "food_type_tag": food_tag_dict['Appetizer'], "cook_style_tags": cook_tag_dict['Grilled'], 
                "taste_tags": [taste_tag_dict['Spicy']], 
                "menu_restriction_tag": [restrict_tag_dict['Keto']], 
                "menu_allergy_tag": [], 
                "ingredients_tag": [ingred_tag_dict['Beef']], 
                "time_of_day_available": "Anytime", "is_modifiable": False
            },
            {
                "item_name": "New MI 1", "average_rating": 7.34, "price": 11.99, "calories": 600, 
                "food_type_tag": food_tag_dict['Dessert'], "cook_style_tags": cook_tag_dict['Baked'], 
                "taste_tags": [taste_tag_dict['Sweet'], taste_tag_dict['Salty']], 
                "menu_restriction_tag": [], 
                "menu_allergy_tag": [allergy_tag_dict['Peanuts']], 
                "ingredients_tag": [ingred_tag_dict['Cheese']], 
                "time_of_day_available": "Anytime", "is_modifiable": False
            },
        ]

        cls.basename = 'menuitems'

        # List URLs (generate a list url for each restaurant being used)
        cls.list_url = []
        for idx in range(0, 3):
            cls.list_url.append(reverse(f'{cls.basename}-list', kwargs={'restaurant_id': idx+1}))

        # Detail URLs
        cls.invalid_rest0_url = reverse(f'{cls.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 10})

        
    def test_list_menuitem_rest(self):
        # Naming Convention: (restaurantaccount)_(owned/notowned)_(restaurantid)_response
        r0_owned_rid1_response = self.client.get(self.list_url[0], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_owned_rid2_response = self.client.get(self.list_url[1], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_notowned_rid3_response = self.client.get(self.list_url[2], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')

        self.assertEqual(r0_owned_rid1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r0_owned_rid1_response.data), 2)
        self.assertEqual(len(r0_owned_rid1_response.data[0]), 6)
        expected_rest = models.Restaurant.objects.get(id=1)
        for obj in r0_owned_rid1_response.data:
            self.assertEqual(obj['restaurant']['name'], expected_rest.name)

        self.assertEqual(r0_owned_rid2_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r0_owned_rid2_response.data), 1)
        self.assertEqual(len(r0_owned_rid2_response.data[0]), 6)
        expected_rest = models.Restaurant.objects.get(id=2)
        for obj in r0_owned_rid2_response.data:
            self.assertEqual(obj['restaurant']['name'], expected_rest.name)

        self.assertEqual(r0_notowned_rid3_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r0_notowned_rid3_response.data['detail'], "This restaurant does not have access to the specified restaurant's menu items.")


    def test_list_menuitem_nonrest(self):
        admin_response = self.client.get(self.list_url[0], HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(self.list_url[0], HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "This user is not of type restaurant.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patron_response.data["detail"], "This user is not of type restaurant.")

    def test_create_menuitem_rest(self):
        data = self.new_menuitems[0]

        r0_owned_rid1_response = self.client.post(self.list_url[0], data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_notowned_rid3_response = self.client.post(self.list_url[2], data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        
        self.assertEqual(r0_owned_rid1_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r0_owned_rid1_response.data['item_name'], data['item_name'])
        other_owned_rest = models.Restaurant.objects.get(id=2)
        self.assertFalse(models.MenuItem.objects.filter(id=r0_owned_rid1_response.data['id'], restaurant=other_owned_rest).exists())
        notowned_rest = models.Restaurant.objects.get(id=3)
        self.assertFalse(models.MenuItem.objects.filter(id=r0_owned_rid1_response.data['id'], restaurant=notowned_rest).exists())

        self.assertEqual(r0_notowned_rid3_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r0_notowned_rid3_response.data['detail'], "This restaurant does not have access to the specified restaurant's menu items.")


    def test_create_menuitem_nonrest(self):
        data = self.new_menuitems[1]

        admin_response = self.client.post(self.list_url[0], data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.post(self.list_url[0], data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "This user is not of type restaurant.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patron_response.data["detail"], "This user is not of type restaurant.")

    def test_retrieve_owned_menuitem_rest(self):
        detail_url_owned = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 1})     
        detail_url_mismatch = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 2, 'pk': 2})  #Wrong RestID for MenuItemID
        detail_url_notowned = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 3, 'pk': 4})  #User does not own RestID
        detail_url_invalid = self.invalid_rest0_url     # MenuItemID has an invalid value (too high)

        r0_owned_rid1_response = self.client.get(detail_url_owned, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_mismatch_rid2_response = self.client.get(detail_url_mismatch, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_notowned_rid3_response = self.client.get(detail_url_notowned, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_invalid_rid1_response = self.client.get(detail_url_invalid, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')

        self.assertEqual(r0_owned_rid1_response.status_code, status.HTTP_200_OK)
        expected_menuitem = models.MenuItem.objects.get(id=1)
        self.assertEqual(r0_owned_rid1_response.data['item_name'], expected_menuitem.item_name)
        self.assertEqual(r0_owned_rid1_response.data['restaurant']['id'], expected_menuitem.restaurant.id)
        
        self.assertEqual(r0_mismatch_rid2_response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(r0_notowned_rid3_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r0_notowned_rid3_response.data['detail'], "This restaurant does not have access to the specified restaurant's menu items.")

        self.assertEqual(r0_invalid_rid1_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_owned_menuitem_nonrest(self):
        detail_url = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 1})

        admin_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "This user is not of type restaurant.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patron_response.data["detail"], "This user is not of type restaurant.")

    def test_retrieve_nonowned_menuitem_allusers(self):
        detail_url = reverse('menuitems-retrieve', kwargs={'pk': 4})

        #None of these users own the menu item with a primary key of 4
        rest0_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        admin_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        expected_menuitem = models.MenuItem.objects.get(id=4)

        self.assertEqual(rest0_response.status_code, status.HTTP_200_OK)
        self.assertEqual(rest0_response.data['item_name'], expected_menuitem.item_name)

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data['item_name'], expected_menuitem.item_name)

        self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patron_response.data['item_name'], expected_menuitem.item_name)

    def test_update_menuitem_rest(self):
        detail_url_owned = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 1})     
        detail_url_mismatch = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 2, 'pk': 2})  #Wrong RestID for MenuItemID
        detail_url_notowned = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 3, 'pk': 4})  #User does not own RestID
        detail_url_invalid = self.invalid_rest0_url     # MenuItemID has an invalid value (too high)

        data = self.new_menuitems[0]

        r0_owned_rid1_response = self.client.put(detail_url_owned, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_mismatch_rid2_response = self.client.put(detail_url_mismatch, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_notowned_rid3_response = self.client.put(detail_url_notowned, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_invalid_rid1_response = self.client.put(detail_url_invalid, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')

        self.assertEqual(r0_owned_rid1_response.status_code, status.HTTP_200_OK)
        # expected_menuitem = models.MenuItem.objects.get(id=1)
        expected_rest = models.Restaurant.objects.get(id=1)
        self.assertEqual(r0_owned_rid1_response.data['item_name'], data['item_name'])
        self.assertEqual(r0_owned_rid1_response.data['restaurant'], expected_rest.id)
        
        self.assertEqual(r0_mismatch_rid2_response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(r0_notowned_rid3_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r0_notowned_rid3_response.data['detail'], "This restaurant does not have access to the specified restaurant's menu items.")

        self.assertEqual(r0_invalid_rid1_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_menuitem_nonrest(self):
        detail_url = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 1})
        data = self.new_menuitems[1]

        admin_response = self.client.put(detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.put(detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "This user is not of type restaurant.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patron_response.data["detail"], "This user is not of type restaurant.")

    def test_delete_menuitem_rest(self):
        detail_url_owned = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 1})     
        detail_url_mismatch = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 2, 'pk': 2})  #Wrong RestID for MenuItemID
        detail_url_notowned = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 3, 'pk': 4})  #User does not own RestID
        detail_url_invalid = self.invalid_rest0_url     # MenuItemID has an invalid value (too high)

        r0_owned_rid1_response = self.client.delete(detail_url_owned, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_mismatch_rid2_response = self.client.delete(detail_url_mismatch, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_notowned_rid3_response = self.client.delete(detail_url_notowned, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        r0_invalid_rid1_response = self.client.delete(detail_url_invalid, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')

        self.assertEqual(r0_owned_rid1_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.MenuItem.objects.filter(id=1).exists())
        
        self.assertEqual(r0_mismatch_rid2_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(models.MenuItem.objects.filter(id=2).exists())

        self.assertEqual(r0_notowned_rid3_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r0_notowned_rid3_response.data['detail'], "This restaurant does not have access to the specified restaurant's menu items.")
        self.assertTrue(models.MenuItem.objects.filter(id=4).exists())

        self.assertEqual(r0_invalid_rid1_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menuitem_nonrest(self):
        detail_url = reverse(f'{self.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 1})

        admin_response = self.client.delete(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.delete(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "This user is not of type restaurant.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patron_response.data["detail"], "This user is not of type restaurant.")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class RestaurantTests(APITestCase):
    fixtures = ['users.json', 'resttags.json', 'restaurants.json']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.restaurant0_user = User.objects.get(email="restaurant0@app.com")
        cls.restaurant0_access = create_jwt_pair_for_user(cls.restaurant0_user)['access']

        cls.restaurant1_user = User.objects.get(email="restaurant1@app.com")
        cls.restaurant1_access = create_jwt_pair_for_user(cls.restaurant1_user)['access']
        
        cls.admin_user = User.objects.get(email="admin@app.com")
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        cls.patron_user = User.objects.get(email="patron@app.com")
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']


        tag_dict = {tag.title: tag.id for tag in models.RestTag.objects.all()}

        # rest_tag_names = models.RestTag.objects.all().values_list('title', flat=True)
        # tag_dict = {name: models.RestTag.objects.get(title=name).id for name in rest_tag_names}     # {'title', 'id'}

        cls.new_data = [{"name": "Buffalo Wild Wings", "rating": 0.05,
            "tags": [tag_dict['Bar'], tag_dict['American']],"price_level": "$$$","phone_number": "757-989-1102",
            "website": "https://www.bww.com","street_name": "124 University Avenue",
            "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"name": "Dairy Queen", "rating": 9.99,
            "tags": [tag_dict['Ice Cream Parlor']],"price_level": "$","phone_number": "757-382-3392",
            "website": "https://www.dq.com","street_name": "125 University Avenue",
            "city": "Norfolk","state": "VA","zip_code": "23529"
            },
        ]

        cls.basename = 'restaurants'
        cls.list_url = reverse(f'{cls.basename}-list') #list and create
        cls.invalid_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 10}) #retrieve, update, delete


    def test_list_restaurants_rest(self):
        
        rest0_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        rest1_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant1_access}')
        
        #Rest0 Tests
        self.assertEqual(rest0_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rest0_response.data), 2)

        rest_owned = list(models.Restaurant.objects.filter(owner=self.restaurant0_user).values_list('id',flat=True))
        for obj in rest0_response.data:
            self.assertTrue(obj["id"] in rest_owned)
            rest_owned.remove(obj["id"])

        self.assertEqual(len(rest_owned), 0)

        #Rest1 Tests
        self.assertEqual(rest1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rest1_response.data), 2)

        rest_owned = list(models.Restaurant.objects.filter(owner=self.restaurant1_user).values_list('id',flat=True))
        for obj in rest1_response.data:
            self.assertTrue(obj["id"] in rest_owned)
            rest_owned.remove(obj["id"])

        self.assertEqual(len(rest_owned), 0)

    def test_list_restaurants_nonrest(self):
        admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    def test_create_restaurants_rest(self):

        rest0_response = self.client.post(self.list_url, self.new_data[0], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        rest1_response = self.client.post(self.list_url, self.new_data[1], HTTP_AUTHORIZATION=f'Bearer {self.restaurant1_access}')

        #Rest0 Tests
        self.assertEqual(rest0_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(rest0_response.data), 26)

        rest_owned = models.Restaurant.objects.filter(owner=self.restaurant0_user)
        self.assertEqual(len(rest_owned), 3)

        self.assertTrue(models.Restaurant.objects.filter(owner=self.restaurant0_user, id=rest0_response.data['id']).exists())
        new_rest = models.Restaurant.objects.get(id=rest0_response.data['id'])
        self.assertEquals(self.new_data[0]["name"], new_rest.name)

        self.assertFalse(models.Restaurant.objects.filter(owner=self.restaurant0_user, id=rest1_response.data['id']).exists())

    def test_create_restaurants_nonrest(self):
        data = self.new_data[1]

        admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    def test_retrieve_restaurants_rest(self):
        
        detail0_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})
        detail1_url = reverse(f'{self.basename}-detail', kwargs={'pk': 3})  #rest1 owns this

        rest0_response = self.client.get(detail0_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        rest0_wrongowner_response = self.client.get(detail1_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        
        self.assertEqual(rest0_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rest0_response.data), 26)

        req_rest = models.Restaurant.objects.get(id=1)
        self.assertEqual(rest0_response.data["name"], req_rest.name)
        self.assertEqual(rest0_response.data["owner"], self.restaurant0_user.id)

        self.assertEqual(rest0_wrongowner_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_restaurants_nonrest(self):
        detail_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})

        admin_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    def test_update_restaurants_rest(self):
        
        detail0_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})
        detail1_url = reverse(f'{self.basename}-detail', kwargs={'pk': 3})  #rest1 owns this

        rest0_response = self.client.put(detail0_url, self.new_data[0], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        rest0_wrongowner_response = self.client.put(detail1_url, self.new_data[1], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        invalid_response = self.client.put(self.invalid_url, self.new_data[1], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        
        self.assertEqual(rest0_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rest0_response.data), 26)
        self.assertEqual(len(models.Restaurant.objects.filter(owner=self.restaurant0_user)), 2)

        req_rest = models.Restaurant.objects.get(id=1)
        self.assertEqual(rest0_response.data["name"], req_rest.name)
        self.assertEqual(rest0_response.data["owner"], self.restaurant0_user.id)

        self.assertEqual(rest0_wrongowner_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_restaurants_nonrest(self):
        detail_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})
        data = self.new_data[1]

        admin_response = self.client.put(detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.put(detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    def test_delete_restaurants_rest(self):
        
        detail0_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})
        detail1_url = reverse(f'{self.basename}-detail', kwargs={'pk': 3})  #rest1 owns this

        rest0_response = self.client.delete(detail0_url, self.new_data[0], HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        rest0_wrongowner_response = self.client.delete(detail1_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        
        self.assertEqual(rest0_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(models.Restaurant.objects.filter(owner=self.restaurant0_user)), 1)
        self.assertFalse(models.Restaurant.objects.filter(id=1).exists())

        self.assertEqual(rest0_wrongowner_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_restaurants_nonrest(self):
        detail_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})

        admin_response = self.client.delete(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.delete(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")


class TagTests(ABC):

    def setUpTestCase(cls):
        cls.TagModel.objects.create(title=cls.tags[0], id=1)
        cls.TagModel.objects.create(title=cls.tags[1], id=2)
        cls.TagModel.objects.create(title=cls.tags[2], id=3)

        cls.admin_user = User.objects.get(email="admin@app.com")
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        cls.restaurant_user = User.objects.get(email="restaurant0@app.com")
        cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

        cls.patron_user = User.objects.get(email="patron@app.com")
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

        cls.list_url = reverse(f'{cls.basename}-list')
        cls.detail_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 1})
        cls.invalid_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 10})


    def test_list_tag_allusers(self):
        """Ensure all users can list out existing rest tags"""

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
        data = {"title":self.tags[3]}

        admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
        self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(self.TagModel.objects.all()), 4)
        self.assertTrue(self.TagModel.objects.filter(title=data['title']).exists())

    def test_create_tag_nonadmin(self):
        """Ensure nonadmin can not create a rest tag"""
        data = {"title":self.tags[4]}

        patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(self.TagModel.objects.all()), 3)
        self.assertFalse(self.TagModel.objects.filter(title=data['title']).exists())

        self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(self.TagModel.objects.all()), 3)
        self.assertFalse(self.TagModel.objects.filter(title=data['title']).exists())

    def test_retrieve_tag_allusers(self):
        """Ensure all users can retrieve a rest tag"""

        admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
        invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data["title"], self.TagModel.objects.get(id=admin_response.data["id"]).title)

        self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patron_response.data["title"], self.TagModel.objects.get(id=patron_response.data["id"]).title)

        self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
        self.assertEqual(rest_response.data["title"], self.TagModel.objects.get(id=rest_response.data["id"]).title)

        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tag_admin(self):
        """Ensure admin can retrieve a rest tag"""
        data = {"title":self.tags[3]}

        admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data["title"], data["title"])
        self.assertEqual(self.TagModel.objects.get(id=admin_response.data["id"]).title, data["title"])

        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tag_nonadmin(self):
        """Ensure nonadmin can not retrieve a rest tag"""
        data = {"title":self.tags[4]}

        patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.TagModel.objects.filter(title=data['title']).exists())

        self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.TagModel.objects.filter(title=data['title']).exists())

    def test_delete_tag_admin(self):
        """Ensure admin can delete a rest tag"""
        response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        deleted_data = response.data["title"]

        admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(self.TagModel.objects.all()), 2)
        self.assertFalse(self.TagModel.objects.filter(title=deleted_data).exists())

        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_tag_nonadmin(self):
        """Ensure nonadmin can not delete a rest tag"""
        patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
        rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

    
    def tearDownTestCase(cls):
        cls.TagModel.objects.all().delete()


class RestTagTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.RestTag
    basename = 'resttags'
    tags = ['Mexican', 'Fast Food', 'Bar', 'Thai', 'Mongolian']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()


class FoodTypeTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.FoodTypeTag
    basename = 'foodtypetags'
    tags = ['Appetizer', 'Beverage', 'Entree', 'Dessert', 'Alcoholic Beverage']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()


class CookStyleTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.CookStyleTag
    basename = 'cookstyletags'
    tags = ['Boiled', 'Steamed', 'Grilled', 'Baked', 'Fried']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()


class TasteTagTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.TasteTag
    basename = 'tastetags'
    tags = ['Sweet', 'Salty', 'Spicy', 'Umami', 'Bitter']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()


class RestrictionTagTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.RestrictionTag
    basename = 'restrictiontags'
    tags = ['Kosher', 'Halal', 'Vegan', 'Vegetarian', 'Keto']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()


class AllergyTagTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.AllergyTag
    basename = 'allergytags'
    tags = ['Milk', 'Peanuts', 'Shellfish', 'Sesame', 'Wheat']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()


class IngredientTagTests(APITestCase, TagTests):
    fixtures = ['users.json']

    TagModel = models.IngredientTag
    basename = 'ingredienttags'
    tags = ['Beef', 'Lettuce', 'Cheese', 'Tomato', 'Bread']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
        super().tearDownClass()
