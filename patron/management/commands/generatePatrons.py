# Import statements
from faker import Faker
import random  # Import the random module

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
    
        data_list = []
        for _ in range(count):
            #Generate and Store Data
            data = {
                "email" : self.fake.email(),
                "password" : "password",
                "name": self.fake.name(),
                "dob" : str(self.fake.date_of_birth(minimum_age=18, maximum_age=70)),
                "calorie_limit" : int(self.fake.random_int(min=200, max=1500)),
                "gender" : self.fake.random_element(elements=('Male', 'Female', 'Other')),
                "price_preference": self.fake.random_element(elements=('$', '$$', '$$$')),
                "zip_code": random.choice(valid_vb_zip_codes),
            }

            data_list.append(data)

        return data_list