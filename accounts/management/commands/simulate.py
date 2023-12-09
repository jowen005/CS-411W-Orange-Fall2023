from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta
from faker import Faker

import json
from pathlib import Path

import restaurants.models as rm
from patron.models import Patron
from analytics.models import LoginRecord



class Command(BaseCommand):

    help = 'Simulate Traffic and Analytic/Trend Generation.'
    User = get_user_model()
    fake = Faker()

    def add_arguments(self, parser: CommandParser):
        pass
        # parser.add_argument("email", nargs=1, type=str)
        # parser.add_argument('-n', dest='num_searches', default=1, type=int, 
        #                     help='Specifies a number of searches')

    def handle(self, *args, **kwargs):
        APP_DIR = Path(__file__).resolve().parent.parent

        #decide if this is first run (check global analytics for num of objects)
        # if num of global analytics < 5
            # get current date time
            # initialize list of days for 7 days ago to 1 day ago (days 1-7)
            # generate traffic for days 1-3 and take analytic with day 4 as current
            # generate traffic for day 4 and take analytic with day 5 as current
            # generate traffic for day 5 and take analytic with day 6 as current
            # generate traffic for day 6 and take analytic with day 7 as current

        # generate traffic for day 8 and take analytic with TODAY as current
        # generate trends for all analytics










        # patron_accounts = self.User.objects.filter(
        #     user_type='patron'
        # ).order_by('id')

        # current = timezone.now()
        # days = [current - timedelta(days=x) for x in range(5)]


        
    

        self.simulate_patron_traffic(patron_accounts)  
        call_command('manualAnalytics')


        self.stdout.write(self.style.SUCCESS(f"The Simulation Succesfully Completed!"))


    def simulate_patron_traffic(self, patron_accounts):
        profile_set = Patron.objects.all()
        for account in patron_accounts:
            try:
                profile_set.get(user=account)
            except Patron.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"This Patron Account {account.email} " + 
                                             "does not have an Associated Patron Profile"))
            
            LoginRecord.objects.create(user=account, date_stamp=current_datestamp)

            NUM_SEARCHES = 10
            call_command('generatePatronTraffic', account.email, '-n', str(NUM_SEARCHES))