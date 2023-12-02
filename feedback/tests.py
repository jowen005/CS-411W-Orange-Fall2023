from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from . import models
from restaurants.models import Restaurant, MenuItem
from django.contrib.auth import get_user_model
from accounts.tokens import create_jwt_pair_for_user

User = get_user_model()


class ReviewTests(APITestCase):
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

        cls.patron_user = User.objects.get(email="patron@app.com")
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

        cls.rest_dict = {rest.name: rest.id  for rest in Restaurant.objects.all()}

        cls.basename = 'menuitems'

        # List URLs (generate a list url for each restaurant being used)
        cls.list_url = []
        for idx in range(0, 3):
            cls.list_url.append(reverse(f'{cls.basename}-list', kwargs={'restaurant_id': idx+1}))

        # Detail URLs
        cls.invalid_rest0_url = reverse(f'{cls.basename}-detail', kwargs={'restaurant_id': 1, 'pk': 10})

    # test review :
    # able to be created, 
    # created by correct patron, 
    # avg rating calculation correct
    # the formatted_datetime method returns a formatted string
    def test_review_menu_item(self):
        # Authenticate a valid patron
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.patron_access}')

        # Create a test menu item
        test_menu_item = MenuItem.objects.create(
            item_name='Test Item',
            restaurant=Restaurant.objects.first(),
            average_rating=0.0,
            price=10.0,
            calories=500,
            time_of_day_available='Anytime',
            is_modifiable=False
        )

        # Post a review by the authenticated patron
        response = self.client.post(
            reverse('feedback-list'),  
            data={
                'patron': self.patron_user.id,
                'menu_item': test_menu_item.id,
                'review': 'This is a test review.',
                'rating': 5.0  
            },
            format='json'
        )

        # Check that the review was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Failed to create a review")

        # Check that the average rating for the associated menu item is updated
        test_menu_item.refresh_from_db()
        self.assertEqual(test_menu_item.average_rating, 5.0, "Rating not updated correctly")

        # Check that the review was created by the correct patron
        review = models.Reviews.objects.get(id=response.data['id'])
        self.assertEqual(review.patron, self.patron_user, "Review not created by the correct patron")

        # Check that the formatted_datetime method returns a formatted string
        formatted_datetime = review.formatted_datetime()
        self.assertIsInstance(formatted_datetime, str)
        self.assertRegex(formatted_datetime, r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')

         # Post the second review by the authenticated patron
        response2 = self.client.post(
            reverse('feedback-list'),
            data={
                'patron': self.patron_user.id,
                'menu_item': test_menu_item.id,
                'review': 'This is the second test review.',
                'rating': 3.0
            },
            format='json'
        )

        # Check that the second review was created successfully
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED, "Failed to create the second review")

        # Check that the average rating for the associated menu item is updated after the second review
        test_menu_item.refresh_from_db()
        self.assertEqual(test_menu_item.average_rating, 4.0, "Rating not updated correctly after the second review")

        # Check that the second review was created by the correct patron
        review2 = models.Reviews.objects.get(id=response2.data['id'])
        self.assertEqual(review2.patron, self.patron_user, "Second review not created by the correct patron")

        # Check that the formatted_datetime method returns a formatted string
        formatted_datetime = review2.formatted_datetime()
        self.assertIsInstance(formatted_datetime, str)
        self.assertRegex(formatted_datetime, r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')

class AppSatisfactionTests(APITestCase):
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

        cls.patron_user = User.objects.get(email="patron@app.com")
        cls.patron_access = create_jwt_pair_for_user(cls.patron_user)['access']

    #restaurant user able to write Satisfaction
    #patron user able to write Satisfaction
    def test_create_app_satisfaction(self):
        # Create an AppSatisfaction instance for restaurant0
        app_satisfaction_restaurant0 = models.AppSatisfaction.objects.create(
            user=self.restaurant0_user,
            review='This is a test review for the app by restaurant0.',
            rating=4.5
        )

        # Check that the AppSatisfaction instance for restaurant0 is created successfully
        self.assertIsInstance(app_satisfaction_restaurant0, models.AppSatisfaction)

        # Check the attributes of the created instance for restaurant0
        self.assertEqual(app_satisfaction_restaurant0.user, self.restaurant0_user)
        self.assertEqual(app_satisfaction_restaurant0.review, 'This is a test review for the app by restaurant0.')
        self.assertEqual(app_satisfaction_restaurant0.rating, 4.5)

        # Create an AppSatisfaction instance for restaurant1
        app_satisfaction_restaurant1 = models.AppSatisfaction.objects.create(
            user=self.restaurant1_user,
            review='This is a test review for the app by restaurant1.',
            rating=3.0
        )

        # Check that the AppSatisfaction instance for restaurant1 is created successfully
        self.assertIsInstance(app_satisfaction_restaurant1, models.AppSatisfaction)

        # Check the attributes of the created instance for restaurant1
        self.assertEqual(app_satisfaction_restaurant1.user, self.restaurant1_user)
        self.assertEqual(app_satisfaction_restaurant1.review, 'This is a test review for the app by restaurant1.')
        self.assertEqual(app_satisfaction_restaurant1.rating, 3.0)

        # Create an AppSatisfaction instance for patron
        app_satisfaction_patron = models.AppSatisfaction.objects.create(
            user=self.patron_user,
            review='This is a test review for the app by patron0.',
            rating=5.0
        )

        # Check that the AppSatisfaction instance for patron is created successfully
        self.assertIsInstance(app_satisfaction_patron, models.AppSatisfaction)

        # Check the attributes of the created instance for patron
        self.assertEqual(app_satisfaction_patron.user, self.patron_user)
        self.assertEqual(app_satisfaction_patron.review, 'This is a test review for the app by patron0.')
        self.assertEqual(app_satisfaction_patron.rating, 5.0)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()