from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command


class Command(BaseCommand):

    help = 'Executes all Trend Algorithms manually.'

    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)

    def handle(self, *args, **options):



        self.stdout.write(self.style.SUCCESS(f'All Trend Algorithms were run'))