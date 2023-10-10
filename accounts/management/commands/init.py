from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command

class Command(BaseCommand):

    help = 'Calls the appropriate load functions to initialize the database'


    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)


    def handle(self, *args, **options):
        
        call_command('loadAccounts')
        call_command('loadMenuTags')
        

        self.stdout.write(self.style.SUCCESS(f'All commands were called'))

    