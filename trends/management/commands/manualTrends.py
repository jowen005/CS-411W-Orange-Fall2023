from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command

import trends.utils.filter_trends as ft
import trends.utils.menu_item_trends as mt
import trends.utils.satisfaction_trends as st


class Command(BaseCommand):

    help = 'Executes all Trend Algorithms manually.'

    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)

    def handle(self, *args, **options):

        ft.driver()
        # mt.driver()
        # st.driver()

        self.stdout.write(self.style.SUCCESS(f'All Trend Algorithms were run'))