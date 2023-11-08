from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command

class Command(BaseCommand):

    help = 'Calls the generate and load function for restaurants'


    def add_arguments(self, parser: CommandParser):
        parser.add_argument("count", nargs=1, type=int)


    def handle(self, count, *args, **options):

        if count[0] <= 0:
            self.stdout.write(self.style.ERROR(f'Supply a positive count!'))
            exit()

        call_command('generateRestaurants', str(count[0]))
        call_command('loadRestaurants')

        self.stdout.write(self.style.SUCCESS(f'{count[0]} restaurant object(s) were added to the database'))
