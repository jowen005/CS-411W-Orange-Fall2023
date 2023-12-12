from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command

class Command(BaseCommand):

    help = 'Calls the appropriate update functions to re-save Patron, Menu Item, Search History, and Review objects.'


    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)


    def handle(self, *args, **options):
        print('Update Calorie Levels in Patron, Menu Item, and Search History objects:')
        call_command('updateCalorieLevels')
        print('\nUpdate Patron Names in Review objects:')
        call_command('updateFeedback')
        print('\nUpdate Taste Vectors in Patron and Menu Item objects:')
        call_command('updateVectors')
        

        self.stdout.write(self.style.SUCCESS(f'All commands were called'))