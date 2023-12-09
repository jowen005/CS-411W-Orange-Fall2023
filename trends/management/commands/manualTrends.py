from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from datetime import datetime

import trends.utils.filter_trends as ft
import trends.utils.menu_item_trends as mt
import trends.utils.satisfaction_trends as st


class Command(BaseCommand):

    help = 'Executes all Trend Algorithms manually.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-d', dest='sim_datetime', default=None, 
                            help='Specifies a datetime to simulate trends from.',)

    def handle(self, sim_datetime, *args, **options):

        if sim_datetime is not None:
            datetime_format = "%Y-%m-%d_%H:%M:%S"
            sim_datetime = datetime.strptime(sim_datetime, datetime_format)

        ft.driver(sim_datetime)
        mt.driver(sim_datetime)
        st.driver(sim_datetime)

        self.stdout.write(self.style.SUCCESS(f'All Trend Algorithms were run'))