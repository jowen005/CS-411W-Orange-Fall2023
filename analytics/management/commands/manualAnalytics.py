from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command

import analytics.utils.exclusion_analysis as ea
import analytics.utils.global_analysis as ga
import analytics.utils.calorie_analysis as ca
import analytics.utils.tag_analysis as ta
import analytics.utils.overall_filter_analysis as ofa
import analytics.utils.menu_item_analysis as ma
import analytics.utils.satisfaction_analysis as sa

class Command(BaseCommand):

    help = 'Calls the appropriate load functions to initialize the database'

    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)

    def handle(self, *args, **options):
        
        ea.driver

        # ga.driver()
        # ca.driver()
        # ta.driver()
        # ofa.driver()
        # ma.driver()
        # sa.driver()

        self.stdout.write(self.style.SUCCESS(f'All Analytics were run'))