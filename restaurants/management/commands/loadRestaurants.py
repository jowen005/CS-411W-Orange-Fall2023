from django.core.management.base import BaseCommand, CommandParser
from restaurants.models import Restaurant, RestTag
from django.contrib.auth import get_user_model
import json
from pathlib import Path

DEFAULT_JSON_PATH = 'json_files/restaurantBuffer.json'

User = get_user_model()
class Command(BaseCommand):
    help = 'Generate and insert fake patron user data'
    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-f', dest='json_path', default=DEFAULT_JSON_PATH, 
                            help='Specifies a file to load',)


    def handle(self, *args, **options):
        
        if options['json_path'] == DEFAULT_JSON_PATH:
            APP_DIR = Path(__file__).resolve().parent.parent
            json_path = APP_DIR + options['json_path']
        else:
            json_path = options['json_path']
        
        #Input Data
        try:
            with open(APP_DIR/json_path) as infile:
                data_list = json.load(infile)
        except IOError:
            print("ERROR")
            data_list = {}

        self.load(data_list)

        self.stdout.write(self.style.SUCCESS(f'All Objects were successfully loaded'))


    def load(self, data_list):
        for obj in data_list:
            #All PK Field Attributes must be popped off
            owner_id = obj.pop('owner')
            tag_ids = obj.pop('tags')
            
            #Retrieve objects references by PKFields
            owner = User.objects.get(pk=owner_id)   # Format for ForeignKey/OneToOneFields
            tags = [RestTag.objects.get(pk=tag_id) for tag_id in tag_ids]   #Format for ManyToManyFields

            #Create object
            rest = Restaurant.objects.create(owner=owner, **obj)
            rest.tags.set(tags)