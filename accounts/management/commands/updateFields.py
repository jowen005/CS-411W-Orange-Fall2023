from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):

    help = 'Calls the appropriate update functions to re-save Patron, Menu Item, Search History, and Review objects.'


    def handle(self, *args, **options):
        print('Update Calorie Levels in Patron, Menu Item, and Search History objects:')
        call_command('updateCalorieLevels')
        print('\nUpdate Patron Names in Review objects:')
        call_command('updateFeedback')
        print('\nUpdate Taste Vectors in Patron and Menu Item objects:')
        call_command('updateVectors')
        

        self.stdout.write(self.style.SUCCESS(f'All commands were called'))

