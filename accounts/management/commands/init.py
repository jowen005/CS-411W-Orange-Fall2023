from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):

    help = 'Calls the appropriate load functions to initialize the database'

    def handle(self, *args, **options):
        
        call_command('loadDefaultAccounts')
        call_command('loadMenuTags')
        call_command('loadDefaultPatrons')
        call_command('loadDefaultRestaurants')
        call_command('loadDefaultMenuItem')

        self.stdout.write(self.style.SUCCESS(f'All commands were called'))

    