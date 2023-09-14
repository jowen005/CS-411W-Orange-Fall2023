# Import statements
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from patron.models import Patron
from django.contrib.auth import get_user_model
from faker import Faker
import random  # Import the random module

User = get_user_model()
class Command(BaseCommand):
    help = 'Generate and insert fake patron user data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Define a list of Virginia Beach ZIP codes
        virginia_beach_zip_codes = [
            '23450', '23451', '23452', '23453', '23454',
            '23455', '23456', '23457', '23458', '23459',
            '23460', '23461', '23462', '23463', '23464',
            '23465', '23466', '23467', '23468', '23471',
            '23479',
        ]

        for _ in range(10):
            # Create a fake user
            username = fake.user_name()
            email = fake.email()
            password = User.objects.make_random_password()
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create a fake patron profile
            name = fake.name()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=70)
            calorie_limit = fake.random_int(min=1200, max=3000)
            gender = fake.random_element(elements=('Male', 'Female', 'Other'))
            price_preference = fake.random_element(elements=('$', '$$', '$$$'))

            # Use a random ZIP code from the Virginia Beach list
            zipcode = random.choice(virginia_beach_zip_codes)

            dietary_restriction = fake.sentence(nb_words=6)
            palate_preference = fake.sentence(nb_words=6)

            Patron.objects.create(
                user=user,
                name=name,
                dob=dob,
                calorie_limit=calorie_limit,
                gender=gender,
                price_preference=price_preference,
                zipcode=zipcode,
                dietary_restriction=dietary_restriction,
                palate_preference=palate_preference
            )

            self.stdout.write(self.style.SUCCESS(f'Created patron user: {username}'))
