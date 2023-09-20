from django.core.management.base import BaseCommand, CommandParser
from restaurants.models import RestTag
from django.contrib.auth import get_user_model
from faker import Faker
import random  # Import the random module
import json
from pathlib import Path

DEFAULT_JSON_PATH = 'json_files/restaurantBuffer.json'

User = get_user_model()
class Command(BaseCommand):
    help = 'Generate and insert fake patron user data'
    def add_arguments(self, parser: CommandParser):
        parser.add_argument("count", nargs=1, type=int)


    def handle(self, count,*args, **kwargs):
        
        count = int(count[0])

        gen_data = self.generate(count)
        
        #Export Data
        APP_DIR = Path(__file__).resolve().parent.parent
        with open(APP_DIR/DEFAULT_JSON_PATH, 'w') as outfile:
            json.dump(gen_data, outfile, indent=4)

        self.stdout.write(self.style.SUCCESS(f'{count} Object(s) were just generated'))


    def generate(self, count:int):
        
        fake = Faker()
        
        #Define Valid Value Constants
        valid_vb_zip_codes = [
            '23450', '23451', '23452', '23453', '23454',
            '23455', '23456', '23457', '23458', '23459',
            '23460', '23461', '23462', '23463', '23464',
            '23465', '23466', '23467', '23468', '23471',
            '23479',
        ]

        #Get Valid Values for PK Field attributes
        valid_owners = list(User.objects.filter(user_type='restaurant').values_list('id',flat=True))
        valid_tags = list(RestTag.objects.values_list('id',flat=True))
        
        data_list = []
        for _ in range(count):
            #Generate and Store Data
            data = {
                "owner": random.choice(valid_owners),
                "name": "A Restaurant Name",
                "rating": float(fake.numerify(text='#.##')),
                "tags": list(set(fake.random_choices(elements=valid_tags))),
                "price_level": fake.random_element(elements=('$', '$$', '$$$')),
                "phone_number": fake.numerify(text='757-###-####'),
                "website": fake.url(),
                "street_name": fake.street_address(),
                "city": "Virginia Beach",
                "state": "VA",
                "zip_code": random.choice(valid_vb_zip_codes),
            }

            data_list.append(data)

        return data_list

    