from django.core.management.base import BaseCommand, CommandParser
from restaurants.models import Restaurant, RestTag
from django.contrib.auth import get_user_model

import json
import inspect
from pathlib import Path
from abc import ABC, abstractmethod


def add_file_path(cls):
    cls.file_path = inspect.getfile(cls)
    return cls

class LoadCommand(BaseCommand, ABC):
    """
        Abstract Base Class for creating Load commands.

        By default uses DEFAULT_JSON_PATHas input, but a file 
        can be specified using the -f=json_path flag

        To implement, do the following:
        * Use @add_file_path decorator before class declaration
            to add in the child class's file path
        * Define DEFAULT_JSON_PATH as 'json_files/______.json'
        * Define a load function that creates model objects
    """

    help = 'Generate and insert fake patron user data'
    DEFAULT_JSON_PATH = ""
    User = get_user_model()


    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
                            help='Specifies a file to load',)


    def handle(self, *args, **options):
        
        if options['json_path'] == self.DEFAULT_JSON_PATH:
            APP_DIR = Path(self.file_path).resolve().parent.parent
            json_path = options['json_path']
        else:
            json_path = options['json_path']
        
        #Input Data
        try:
            with open(APP_DIR/json_path) as infile:
                data_list = json.load(infile)
        except IOError:
            data_list = {}
            self.stdout.write(self.style.ERROR(f"IOError Occurred!"))

        self.load(data_list)

        self.stdout.write(self.style.SUCCESS(f'All Objects were successfully loaded'))

    @abstractmethod
    def load(self, data_list):
        """
            Do the following:

            - Pop off all Primary Key Attributes (IDs)
            - Retrieve objects reference by Primary Key Attributes
                - Ex. for ForeignKey/OneToOne Relationships: owner = self.User.objects.get(pk=owner_id)
                - Ex. for ManyToMany Relationships: tags = [RestTag.objects.get(pk=tag_id) for tag_id in tag_ids]
            - Create the object
                - Ex. for ForeignKey/OneToOne Relationships: rest = Restaurant.objects.create(owner=owner, **obj)
                - Ex. for ManyToMany Relationships: After creating object -> rest.tags.set(tags)
        """
        pass