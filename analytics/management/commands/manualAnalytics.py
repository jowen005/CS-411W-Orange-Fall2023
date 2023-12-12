from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.utils import timezone
from datetime import datetime

import analytics.utils.exclusion_analysis as ea
import analytics.utils.global_analysis as ga
import analytics.utils.calorie_analysis as ca
import analytics.utils.tag_analysis as ta
import analytics.utils.overall_filter_analysis as ofa
import analytics.utils.menu_item_analysis as ma
import analytics.utils.satisfaction_analysis as sa
import analytics.utils.local_restaurant_analysis as lra
import analytics.utils.login_analysis as loga


class Command(BaseCommand):

    help = 'Executes all Analytic Algorithms manually.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-d', dest='sim_datetime', default=None, 
                            help='Specifies a datetime to simulate analytics for.',)

    def handle(self, sim_datetime, *args, **options):

        if sim_datetime is not None:
            datetime_format = "%Y-%m-%d_%H:%M:%S"
            sim_datetime = timezone.make_aware(datetime.strptime(sim_datetime, datetime_format))

        ea.driver(sim_datetime)

        ga.driver(sim_datetime)
        sa.driver(sim_datetime)
        loga.driver(sim_datetime)

        ca.driver(sim_datetime)
        ta.driver(sim_datetime)
        ofa.driver(sim_datetime)

        ma.driver(sim_datetime)
        lra.driver(sim_datetime)

        self.stdout.write(self.style.SUCCESS(f'All Analytic Algorithms were run'))