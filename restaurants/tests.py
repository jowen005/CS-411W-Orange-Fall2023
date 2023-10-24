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
        cls.basename = 'restaurants'

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
                "tags": [cls.rest_tags[2],cls.rest_tags[4]],"price_level": "$$","phone_number": "757-274-9281",
                "website": "https://www.woodys.com/","street_name": "120 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"owner": cls.restaurant0_user, "name": "Moes", "rating": 8.34,
                "tags": [cls.rest_tags[1],cls.rest_tags[3]],"price_level": "$$","phone_number": "757-238-6505",
                "website": "https://www.moes.com","street_name": "121 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"owner": cls.restaurant1_user, "name": "McDonalds", "rating": 1.10,
                "tags": [cls.rest_tags[1],cls.rest_tags[4]],"price_level": "$","phone_number": "757-272-4028",
                "website": "https://www.mcds.com","street_name": "122 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"owner": cls.restaurant1_user, "name": "Arbys", "rating": 2.43,
                "tags": [cls.rest_tags[1],cls.rest_tags[4]],"price_level": "$","phone_number": "757-573-8271",
                "website": "https://www.arbys.com","street_name": "123 University Avenue",
                "city": "Norfolk","state": "VA","zip_code": "23529"
            },
        ]

        for obj in cls.data:
            models.Restaurant.objects.create(obj)

        cls.new_data = [{"name": "Buffalo Wild Wings", "rating": 0.05,
            "tags": [cls.rest_tags[2],cls.rest_tags[4]],"price_level": "$$$","phone_number": "757-989-1102",
            "website": "https://www.bww.com","street_name": "124 University Avenue",
            "city": "Norfolk","state": "VA","zip_code": "23529"
            },
            {"name": "Dairy Queen", "rating": 9.99,
            "tags": [cls.rest_tags[5]],"price_level": "$","phone_number": "757-382-3392",
            "website": "https://dq.com","street_name": "125 University Avenue",
            "city": "Norfolk","state": "VA","zip_code": "23529"
            },
        ]

        cls.list_url = reverse(f'{cls.basename}-list')
        cls.invalid_url = reverse(f'{cls.basename}-detail', kwargs={'pk': 10})

    def test_list_restaurants_rest(self):
        
        rest0_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant0_access}')
        self.assertEqual(rest0_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rest0_response.data), 2)

        tags_owned = list(models.Restaurant.objects.filter(owner=self.restaurant0_user).values_list('id',flat=True))
        for obj in rest0_response.data:
            self.assertTrue(obj["id"] in tags_owned)
            tags_owned.remove(obj["id"])

        self.assertTrue(tags_owned.empty())

        rest1_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant1_access}')
       


    def test_list_restaurants_nonrest(self):
        admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

        self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    # def test_create_restaurants_rest(self):
    #     pass

    # def test_create_restaurants_nonrest(self):
    #     data = self.data[1]

    #     admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
    #     patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

    #     self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    #     self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    # def test_retrieve_restaurants_rest(self):
    #     pass

    # def test_retrieve_restaurants_nonrest(self):
    #     detail_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})

    #     admin_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
    #     patron_response = self.client.get(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

    #     self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    #     self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    # def test_update_restaurants_rest(self):
    #     pass

    # def test_update_restaurants_nonrest(self):
    #     detail_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})
    #     data = data[1]

    #     admin_response = self.client.put(detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
    #     patron_response = self.client.put(detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

    #     self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    #     self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    # def test_delete_restaurants_rest(self):
    #     pass
    
    # def test_delete_restaurants_nonrest(self):
    #     detail_url = reverse(f'{self.basename}-detail', kwargs={'pk': 1})

    #     admin_response = self.client.delete(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
    #     patron_response = self.client.delete(detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

    #     self.assertEqual(admin_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

    #     self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(admin_response.data["detail"], "You do not have permission to perform this action.")

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



# Tag Tests written out without code reuse principles
# class RestTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.RestTag.objects.create(title='Mexican')
#         models.RestTag.objects.create(title='Fast Food')
#         models.RestTag.objects.create(title='Bar')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('resttags-list')
#         cls.detail_url = reverse('resttags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('resttags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing rest tags"""
#         expected = ['Mexican', 'Fast Food', 'Bar']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create a rest tag"""
#         data = {"title":"Thai"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.RestTag.objects.all()), 4)
#         self.assertTrue(models.RestTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create a rest tag"""
#         data = {"title":"Mongolian"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.RestTag.objects.all()), 3)
#         self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.RestTag.objects.all()), 3)
#         self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve a rest tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.RestTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.RestTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.RestTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve a rest tag"""
#         data = {"title":"Thai"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.RestTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve a rest tag"""
#         data = {"title":"Mongolian"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.RestTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete a rest tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.RestTag.objects.all()), 2)
#         self.assertFalse(models.RestTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete a rest tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.RestTag.objects.all().delete()
#         User.objects.all().delete()


# class FoodTypeTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.FoodTypeTag.objects.create(title='Appetizer')
#         models.FoodTypeTag.objects.create(title='Beverage')
#         models.FoodTypeTag.objects.create(title='Entree')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('foodtypetags-list')
#         cls.detail_url = reverse('foodtypetags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('foodtypetags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing food type tags"""
#         expected = ['Appetizer', 'Beverage', 'Entree']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create a food type tag"""
#         data = {"title":"Dessert"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.FoodTypeTag.objects.all()), 4)
#         self.assertTrue(models.FoodTypeTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create a food type tag"""
#         data = {"title":"Alcoholic Beverage"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.FoodTypeTag.objects.all()), 3)
#         self.assertFalse(models.FoodTypeTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.FoodTypeTag.objects.all()), 3)
#         self.assertFalse(models.FoodTypeTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve a food type tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.FoodTypeTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.FoodTypeTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.FoodTypeTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve a food type tag"""
#         data = {"title":"Dessert"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.FoodTypeTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve a food type tag"""
#         data = {"title":"Alcoholic Beverage"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.FoodTypeTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.FoodTypeTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete a food type tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.FoodTypeTag.objects.all()), 2)
#         self.assertFalse(models.FoodTypeTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete a food type tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.FoodTypeTag.objects.all().delete()
#         User.objects.all().delete()


# class CookStyleTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.CookStyleTag.objects.create(title='Boiled')
#         models.CookStyleTag.objects.create(title='Grilled')
#         models.CookStyleTag.objects.create(title='Fried')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('cookstyletags-list')
#         cls.detail_url = reverse('cookstyletags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('cookstyletags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing cook style tags"""
#         expected = ['Boiled', 'Grilled', 'Fried']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create a cook style tag"""
#         data = {"title":"Steamed"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.CookStyleTag.objects.all()), 4)
#         self.assertTrue(models.CookStyleTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create a cook style tag"""
#         data = {"title":"Smoked"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.CookStyleTag.objects.all()), 3)
#         self.assertFalse(models.CookStyleTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.CookStyleTag.objects.all()), 3)
#         self.assertFalse(models.CookStyleTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve a cook style tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.CookStyleTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.CookStyleTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.CookStyleTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve a cook style tag"""
#         data = {"title":"Dessert"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.CookStyleTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve a cook style tag"""
#         data = {"title":"Alcoholic Beverage"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.CookStyleTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.CookStyleTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete a cook style tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.CookStyleTag.objects.all()), 2)
#         self.assertFalse(models.CookStyleTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete a cook style tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.CookStyleTag.objects.all().delete()
#         User.objects.all().delete()


# class TasteTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.TasteTag.objects.create(title='Sour')
#         models.TasteTag.objects.create(title='Sweet')
#         models.TasteTag.objects.create(title='Spicy')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('tastetags-list')
#         cls.detail_url = reverse('tastetags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('tastetags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing taste tags"""
#         expected = ['Sour', 'Sweet', 'Spicy']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create a taste tag"""
#         data = {"title":"Bitter"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.TasteTag.objects.all()), 4)
#         self.assertTrue(models.TasteTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create a taste tag"""
#         data = {"title":"Salty"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.TasteTag.objects.all()), 3)
#         self.assertFalse(models.TasteTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.TasteTag.objects.all()), 3)
#         self.assertFalse(models.TasteTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve a taste tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.TasteTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.TasteTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.TasteTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve a taste tag"""
#         data = {"title":"Bitter"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.TasteTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve a taste tag"""
#         data = {"title":"Salty"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.TasteTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.TasteTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete a taste tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.TasteTag.objects.all()), 2)
#         self.assertFalse(models.TasteTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete a taste tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.TasteTag.objects.all().delete()
#         User.objects.all().delete()


# class RestrictionTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.RestrictionTag.objects.create(title='Kosher')
#         models.RestrictionTag.objects.create(title='Keto')
#         models.RestrictionTag.objects.create(title='Halal')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('restrictiontags-list')
#         cls.detail_url = reverse('restrictiontags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('restrictiontags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing restriction tags"""
#         expected = ['Kosher', 'Keto', 'Halal']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create a restriction tag"""
#         data = {"title":"Vegan"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.RestrictionTag.objects.all()), 4)
#         self.assertTrue(models.RestrictionTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create a restriction tag"""
#         data = {"title":"Paleo"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.RestrictionTag.objects.all()), 3)
#         self.assertFalse(models.RestrictionTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.RestrictionTag.objects.all()), 3)
#         self.assertFalse(models.RestrictionTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve a restriction tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.RestrictionTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.RestrictionTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.RestrictionTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve a restriction tag"""
#         data = {"title":"Vegan"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.RestrictionTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve a restriction tag"""
#         data = {"title":"Paleo"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.RestrictionTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.RestrictionTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete a restriction tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.RestrictionTag.objects.all()), 2)
#         self.assertFalse(models.RestrictionTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete a restriction tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.RestrictionTag.objects.all().delete()
#         User.objects.all().delete()


# class AllergyTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.AllergyTag.objects.create(title='Peanuts')
#         models.AllergyTag.objects.create(title='Shellfish')
#         models.AllergyTag.objects.create(title='Wheat')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('allergytags-list')
#         cls.detail_url = reverse('allergytags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('allergytags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing allergy tags"""
#         expected = ['Peanuts', 'Shellfish', 'Wheat']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create an allergy tag"""
#         data = {"title":"Milk"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.AllergyTag.objects.all()), 4)
#         self.assertTrue(models.AllergyTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create an allergy tag"""
#         data = {"title":"Sesame"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.AllergyTag.objects.all()), 3)
#         self.assertFalse(models.AllergyTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.AllergyTag.objects.all()), 3)
#         self.assertFalse(models.AllergyTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve an allergy tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.AllergyTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.AllergyTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.AllergyTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve an allergy tag"""
#         data = {"title":"Milk"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.AllergyTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve an allergy tag"""
#         data = {"title":"Sesame"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.AllergyTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.AllergyTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete an allergy tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.AllergyTag.objects.all()), 2)
#         self.assertFalse(models.AllergyTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete an allergy tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.AllergyTag.objects.all().delete()
#         User.objects.all().delete()


# class IngredientTagTests(APITestCase):
#     @classmethod
#     def setUpClass(cls):
#         models.IngredientTag.objects.create(title='Beef')
#         models.IngredientTag.objects.create(title='Cheese')
#         models.IngredientTag.objects.create(title='Lettuce')

#         cls.admin_user = User.objects.create_superuser(email="admin@app.com", 
#                             username='admin', password="password", user_type='admin')
#         cls.admin_access = create_jwt_pair_for_user(cls.admin_user)['access']

#         cls.restaurant_user = User.objects.create_user(email="restaurant@app.com", 
#                             username='restaurant', password="password", user_type='restaurant')
#         cls.restaurant_access = create_jwt_pair_for_user(cls.restaurant_user)['access']

#         cls.patron_user = User.objects.create_user(email="patron@app.com", 
#                             username='patron', password="password", user_type='patron')
#         cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

#         cls.list_url = reverse('ingredienttags-list')
#         cls.detail_url = reverse('ingredienttags-detail', kwargs={'pk': 1})
#         cls.invalid_url = reverse('ingredienttags-detail', kwargs={'pk': 10})

#     def test_list_tag_allusers(self):
#         """Ensure all users can list out existing ingredient tags"""
#         expected = ['Beef', 'Cheese', 'Lettuce']

#         admin_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(admin_response.data), 3)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(patron_response.data), 3)
        
#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(rest_response.data), 3)
        
#     def test_create_tag_admin(self):
#         """Ensure admin can create an ingredient tag"""
#         data = {"title":"Tomato"}

#         admin_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        
#         self.assertEqual(admin_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(len(models.IngredientTag.objects.all()), 4)
#         self.assertTrue(models.IngredientTag.objects.filter(title=data['title']).exists())

#     def test_create_tag_nonadmin(self):
#         """Ensure nonadmin can not create an ingredient tag"""
#         data = {"title":"Bread"}

#         patron_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.post(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.IngredientTag.objects.all()), 3)
#         self.assertFalse(models.IngredientTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(len(models.IngredientTag.objects.all()), 3)
#         self.assertFalse(models.IngredientTag.objects.filter(title=data['title']).exists())

#     def test_retrieve_tag_allusers(self):
#         """Ensure all users can retrieve an ingredient tag"""

#         admin_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         patron_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')
#         invalid_response = self.client.get(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], models.IngredientTag.objects.get(id=admin_response.data["id"]).title)

#         self.assertEqual(patron_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(patron_response.data["title"], models.IngredientTag.objects.get(id=patron_response.data["id"]).title)

#         self.assertEqual(rest_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(rest_response.data["title"], models.IngredientTag.objects.get(id=rest_response.data["id"]).title)

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_admin(self):
#         """Ensure admin can retrieve an ingredient tag"""
#         data = {"title":"Tomato"}

#         admin_response = self.client.put(self.detail_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.put(self.invalid_url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(admin_response.data["title"], data["title"])
#         self.assertEqual(models.IngredientTag.objects.get(id=admin_response.data["id"]).title, data["title"])

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_tag_nonadmin(self):
#         """Ensure nonadmin can not retrieve an ingredient tag"""
#         data = {"title":"Bread"}

#         patron_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.put(self.list_url, data, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.IngredientTag.objects.filter(title=data['title']).exists())

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertFalse(models.IngredientTag.objects.filter(title=data['title']).exists())

#     def test_delete_tag_admin(self):
#         """Ensure admin can delete an ingredient tag"""
#         response = self.client.get(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         deleted_data = response.data["title"]

#         admin_response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
#         invalid_response = self.client.delete(self.invalid_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')

#         self.assertEqual(admin_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(len(models.IngredientTag.objects.all()), 2)
#         self.assertFalse(models.IngredientTag.objects.filter(title=deleted_data).exists())

#         self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_delete_tag_nonadmin(self):
#         """Ensure nonadmin can not delete an ingredient tag"""
#         patron_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')
#         rest_response = self.client.delete(self.list_url, HTTP_AUTHORIZATION=f'Bearer {self.restaurant_access}')

#         self.assertEqual(patron_response.status_code, status.HTTP_403_FORBIDDEN)

#         self.assertEqual(rest_response.status_code, status.HTTP_403_FORBIDDEN)

#     @classmethod
#     def tearDownClass(cls):
#         models.IngredientTag.objects.all().delete()
#         User.objects.all().delete()


