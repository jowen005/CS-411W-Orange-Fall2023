from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from faker import Faker

import json
import inspect
from pathlib import Path
from abc import ABC, abstractmethod


def add_file_path(cls):
    cls.file_path = inspect.getfile(cls)
    return cls


class GenerateCommand(BaseCommand, ABC):
    """
        Abstract Base Class for creating Generate commands
        * Use @add_file_path decorator before class declaration
            to add in the child class's file path
        * Define DEFAULT_JSON_PATH as 'json_files/______.json'
        * Define a generate function that takes in a count and 
            returns a list of dictionaries containing model data

    """
    help = 'Generate and insert fake patron user data'
    DEFAULT_JSON_PATH = ""
    User = get_user_model()
    fake = Faker()


    def add_arguments(self, parser: CommandParser):
        parser.add_argument("count", nargs=1, type=int)


    def handle(self, count,*args, **kwargs):
        
        count = int(count[0])

        gen_data = self.generate(count)
        
        #Export Data
        APP_DIR = Path(self.file_path).resolve().parent.parent
        with open(APP_DIR/self.DEFAULT_JSON_PATH, 'w') as outfile:
            json.dump(gen_data, outfile, indent=4)

        self.stdout.write(self.style.SUCCESS(f'{count} Object(s) were just generated'))

    @abstractmethod
    def generate(self, count:int):
        """
            Define the following:
            * Valid Value Constants
            * Valid Values for PK Field attributes

            Then generate and store the data in a list of dictionaries
        """
        pass
