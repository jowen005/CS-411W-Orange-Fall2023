from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from . import models
from django.contrib.auth import get_user_model
from accounts.tokens import create_jwt_pair_for_user
from abc import ABC

User = get_user_model()


class RestaurantTests(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        

        cls.restaurant0_user = User.objects.create_user(email="restaurant0@app.com", 
                            username='restaurant', password="password", user_type='restaurant')
        cls.restaurant0_access = create_jwt_pair_for_user(cls.restaurant0_user)['access']

        cls.restaurant1_user = User.objects.create_user(email="restaurant1@app.com", 
                            username='restaurant', password="password", user_type='restaurant')
        cls.restaurant1_access = create_jwt_pair_for_user(cls.restaurant1_user)['access']
        
        cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
                            username='admin', password="password", user_type='admin')
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        cls.patron_user = User.objects.create_user(email="patron@app.com", 
                            username='patron', password="password", user_type='patron')
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

        cls.rest_tag_names = ["Fast Food", "Bar", "Southwest", "American", "Ice Cream Parlor"]
        cls.rest_tags = []

        for tag in cls.rest_tag_names:
            models.RestTag.objects.create(title=tag)
            cls.rest_tags.append(models.RestTag.objects.get(title=tag))

    
        cls.data = [
            {"owner": cls.restaurant0_user, "name": "Woodys", "rating": 4.56,
                "tags": [cls.rest_tags[1],cls.rest_tags[3]],"price_level": "$$","phone_number": "757-274-9281",
                "website": "https://www.woodys.com/","street_name": "120 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"owner": cls.restaurant0_user, "name": "Moes", "rating": 8.34,
                "tags": [cls.rest_tags[0],cls.rest_tags[2]],"price_level": "$$","phone_number": "757-238-6505",
                "website": "https://www.moes.com","street_name": "121 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"owner": cls.restaurant1_user, "name": "McDonalds", "rating": 1.10,
                "tags": [cls.rest_tags[0],cls.rest_tags[3]],"price_level": "$","phone_number": "757-272-4028",
                "website": "https://www.mcds.com","street_name": "122 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"owner": cls.restaurant1_user, "name": "Arbys", "rating": 2.43,
                "tags": [cls.rest_tags[0],cls.rest_tags[3]],"price_level": "$","phone_number": "757-573-8271",
                "website": "https://www.arbys.com","street_name": "123 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
        ]

        for obj in cls.data:
            tags = obj.pop('tags')
            instance = models.Restaurant.objects.create(**obj)
            instance.tags.set(tags)

        cls.new_data = [{"name": "Buffalo Wild Wings", "rating": 0.05,
            "tags": [cls.rest_tags[1].id, cls.rest_tags[3].id],"price_level": "$$$","phone_number": "757-989-1102",
            "website": "https://www.bww.com","street_name": "124 University Avenue",
            "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"name": "Dairy Queen", "rating": 9.99,
            "tags": [cls.rest_tags[4].id],"price_level": "$","phone_number": "757-382-3392",
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
        data = self.data[1]

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

    @classmethod
    def tearDownClass(cls):
        models.Restaurant.objects.all().delete()
        models.RestTag.objects.all().delete()
        User.objects.all().delete()


class TagTests(ABC):

    def setUpTestCase(cls):
        cls.TagModel.objects.create(title=cls.tags[0])
        cls.TagModel.objects.create(title=cls.tags[1])
        cls.TagModel.objects.create(title=cls.tags[2])

        cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
                            username='admin', password="password", user_type='admin')
        cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

        cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
                            username='restaurant', password="password", user_type='restaurant')
        cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

        cls.patron_user = User.objects.create_user(email="patron@app.com", 
                            username='patron', password="password", user_type='patron')
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
        User.objects.all().delete()


class RestTagTests(APITestCase, TagTests):
    TagModel = models.RestTag
    basename = 'resttags'
    tags = ['Mexican', 'Fast Food', 'Bar', 'Thai', 'Mongolian']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)


class FoodTypeTests(APITestCase, TagTests):
    TagModel = models.FoodTypeTag
    basename = 'foodtypetags'
    tags = ['Appetizer', 'Beverage', 'Entree', 'Dessert', 'Alcoholic Beverage']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)


class CookStyleTests(APITestCase, TagTests):
    TagModel = models.CookStyleTag
    basename = 'cookstyletags'
    tags = ['Boiled', 'Steamed', 'Grilled', 'Baked', 'Fried']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)


class TasteTagTests(APITestCase, TagTests):
    TagModel = models.TasteTag
    basename = 'tastetags'
    tags = ['Sweet', 'Salty', 'Spicy', 'Umami', 'Bitter']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)


class RestrictionTagTests(APITestCase, TagTests):
    TagModel = models.RestrictionTag
    basename = 'restrictiontags'
    tags = ['Kosher', 'Halal', 'Vegan', 'Vegetarian', 'Keto']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)


class AllergyTagTests(APITestCase, TagTests):
    TagModel = models.AllergyTag
    basename = 'allergytags'
    tags = ['Milk', 'Peanuts', 'Shellfish', 'Sesame', 'Wheat']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)


class IngredientTagTests(APITestCase, TagTests):
    TagModel = models.IngredientTag
    basename = 'ingredienttags'
    tags = ['Beef', 'Lettuce', 'Cheese', 'Tomato', 'Bread']
    
    @classmethod
    def setUpClass(cls):
        cls.setUpTestCase(cls)
        
    @classmethod
    def tearDownClass(cls):
        cls.tearDownTestCase(cls)
