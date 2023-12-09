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
from analytics.models import LoginRecord, GlobalAnalytics


DATETIME_STR_FORMAT = "%Y-%m-%d_%H:%M:%S"


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

        patron_accounts = self.retrieve_valid_accounts()

        today = timezone.now()
        if GlobalAnalytics.objects.all().count() < 5:
            self.simulate_past_data(today, patron_accounts)

        self.simulate_today(today, patron_accounts)

        call_command('manualTrends', '-d', today.strftime(DATETIME_STR_FORMAT))

        self.stdout.write(self.style.SUCCESS(f"The Simulation Succesfully Completed!"))


    def retrieve_valid_accounts(self):
        profile_set = Patron.objects.all()
        valid_patron_accounts = self.User.objects.filter(
            user_type='patron',
            user__in=profile_set.values('user')
        ).order_by('id')

        return valid_patron_accounts


    def simulate_past_data(self, today, patron_accounts):
        
        days = [today - timedelta(days=x) for x in range(1,8)]
        days.reverse() # Days Increasing from 7 days ago to 1 day ago

        for idx in range(len(days)):
            date = days[idx]
            date_str = date.strftime(DATETIME_STR_FORMAT)
            num_days_simulated = idx

            # patron traffic for current day
            self.simulate_patron_traffic(patron_accounts, date, date_str) 
            
            if num_days_simulated >= 3:
                call_command('manualAnalytics', '-d', date_str)


    def simulate_today(self, today, patron_accounts):
        today_str = today.strftime(DATETIME_STR_FORMAT)
        
        self.simulate_patron_traffic(patron_accounts, today, today_str)
        
        call_command('manualAnalytics', '-d', today_str)


    def simulate_patron_traffic(self, patron_accounts, date, date_str):
        
        for account in patron_accounts:
            #TODO: Do we want multiple logins a day? Do we want a random number if so?
            LoginRecord.objects.create(user=account, date_stamp=date)

            #TODO: Do we want random number of searches?
            NUM_SEARCHES = 10
            call_command('generatePatronTraffic', account.email, 
                         '-n', str(NUM_SEARCHES),
                         '-d', date_str)