# Import statements
import random
from restaurants.models import RestrictionTag, AllergyTag, TasteTag

from lcc_project.commands.generate import GenerateCommand, add_file_path


@add_file_path
class Command(GenerateCommand):
    DEFAULT_JSON_PATH = 'json_files/patronBuffer.json'

    def generate(self, count:int):

        # Define a list of Virginia Beach ZIP codes
        valid_vb_zip_codes = [
            '23450', '23451', '23452', '23453', '23454',
            '23455', '23456', '23457', '23458', '23459',
            '23460', '23461', '23462', '23463', '23464',
            '23465', '23466', '23467', '23468', '23471',
            '23479',
        ]
        
        #Get Valid Values for PK Field attributes
        valid_restriction_tags = list(RestrictionTag.objects.values_list('id',flat=True))
        valid_allergy_tags = list(AllergyTag.objects.values_list('id',flat=True))
        valid_taste_tags = list(TasteTag.objects.values_list('id',flat=True))

        data_list = []
        for _ in range(count):
            force_vegan = random.choices([True, False], weights=[5, 3], k=1)[0]
            vegan_tag_id = RestrictionTag.objects.get(title='vegan').id
            
            restrict_tag_ids = list(set(self.fake.random_choices(elements=valid_restriction_tags)))

            if vegan_tag_id not in restrict_tag_ids and force_vegan == True:
                restrict_tag_ids.append(vegan_tag_id)

            #Generate and Store Data
            email = self.fake.email()
            data = {
                "email" : email,
                "username": email.split('@')[0],
                "password" : "password",
                "name": self.fake.name(),
                "dob" : str(self.fake.date_of_birth(minimum_age=18, maximum_age=70)),
                "calorie_limit" : int(self.fake.random_int(min=200, max=1500)),
                "gender" : self.fake.random_element(elements=('Male', 'Female', 'Other')),
                "price_max": int(self.fake.random_int(min=10, max=100)),
                "zipcode": random.choice(valid_vb_zip_codes),
                "patron_restriction_tag": restrict_tag_ids,
                "patron_allergy_tag": list(set(self.fake.random_choices(elements=valid_allergy_tags))),
                "patron_taste_tag": list(set(self.fake.random_choices(elements=valid_taste_tags))),
            }

            data_list.append(data)

        return data_list
    
    