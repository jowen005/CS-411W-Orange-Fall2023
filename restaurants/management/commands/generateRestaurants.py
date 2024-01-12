import random

from lcc_project.commands.generate import GenerateCommand, add_file_path
from restaurants.models import RestTag

@add_file_path
class Command(GenerateCommand):
    DEFAULT_JSON_PATH = 'json_files/restaurantBuffer.json'

    def generate(self, count:int):

        #Define Valid Value Constants
        valid_vb_zip_codes = [
            '23450', '23451', '23452', '23453', '23454',
            '23455', '23456', '23457', '23458', '23459',
            '23460', '23461', '23462', '23463', '23464',
            '23465', '23466', '23467', '23468', '23471',
            '23479',
        ]

        valid_rest_suffix = [
            '', 'Grill', 'Diner', 'Sushi', 'Bar', 'Smokehouse', 'BBQ', 
            'Pizza', 'Wings', 'Hotdogs', 'Cafe', 'Coffee Shop', 'Steakhouse']

        #Get Valid Values for PK Field attributes
        monarch_acc_id = self.User.objects.get(email='monarch@odu.edu').id

        valid_owners = list(self.User.objects.filter(user_type='restaurant').values_list('id',flat=True))
        valid_owners.remove(monarch_acc_id)

        valid_tags = list(RestTag.objects.values_list('id',flat=True))
        
        data_list = []
        for _ in range(count):
            #Generate and Store Data
            data = {
                "owner": random.choice(valid_owners),
                "name": f"{self.fake.first_name()}'s {random.choice(valid_rest_suffix)}".rstrip(),
                "rating": float(self.fake.numerify(text='#.##')),
                "tags": list(set(self.fake.random_choices(elements=valid_tags))),
                "price_level": self.fake.random_element(elements=('$', '$$', '$$$')),
                "phone_number": self.fake.numerify(text='757-###-####'),
                "website": self.fake.url(),
                "street_name": self.fake.street_address(),
                "city": "Virginia Beach",
                "state": "VA",
                "zip_code": random.choice(valid_vb_zip_codes),
                "mon_open":"08:00:00",
                "mon_close":"23:00:00",
                "tue_open":"08:00:00",
                "tue_close":"23:00:00",
                "wed_open":"08:00:00",
                "wed_close":"23:00:00",
                "thu_open":"08:00:00",
                "thu_close":"23:00:00",
                "fri_open":"08:00:00",
                "fri_close":"23:00:00",
                "sat_open":"08:00:00",
                "sat_close":"23:00:00",
                "sun_open":"08:00:00",
                "sun_close":"23:00:00",
            }

            data_list.append(data)

        return data_list

