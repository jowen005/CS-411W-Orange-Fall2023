from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta
from faker import Faker
from datetime import datetime
import random

from patron.models import Patron, PatronSearchHistory, Bookmark, MenuItemHistory
from feedback.models import Reviews
from analytics.models import LoginRecord, GlobalAnalytics
import analytics.utils.clear_analytics as clear_analytics
import trends.utils.clear_trends as clear_trends


LOGIN_COUNTS = [1, 2]
LOGIN_WEIGHTS = [1, 1]

SEARCH_COUNTS = [3, 4, 5, 6]
SEARCH_WEIGHTS = [1, 1, 1, 1]

DATETIME_STR_FORMAT = "%Y-%m-%d_%H:%M:%S"

NUM_DAYS_BACK = 8


class Command(BaseCommand):

    help = 'Simulate Traffic and Analytic/Trend Generation.'
    User = get_user_model()
    fake = Faker()

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('--soft_reset', action='store_true', help='Soft Reset')
        parser.add_argument('--hard_reset', action='store_true', help='Hard Reset')

    def handle(self, *args, **options):

        self.check_flags(options)
        
        patron_accounts, rest_accounts = self.retrieve_valid_accounts()

        today = timezone.now()
        if GlobalAnalytics.objects.all().count() < 5 and not options['soft_reset']:
            self.simulate_past_data(today, patron_accounts, rest_accounts)

        self.simulate_today(today, patron_accounts, rest_accounts)

        self.stdout.write(self.style.SUCCESS(f"The Simulation Succesfully Completed!"))


    def retrieve_valid_accounts(self):
        profile_set = Patron.objects.all()
        valid_patron_accounts = self.User.objects.filter(
            user_type='patron',
            id__in=profile_set.values('user__id')
        ).order_by('id')

        valid_rest_accounts = self.User.objects.filter(
            user_type='restaurant',
        ).order_by('id')

        return valid_patron_accounts, valid_rest_accounts


    def simulate_past_data(self, today, patron_accounts, rest_accounts):
        print('*'*50) #NOTE
        print("Simulating Past Data") #NOTE
        print('*'*50 + '\n') #NOTE
        
        days = [today - timedelta(days=x) for x in range(1,NUM_DAYS_BACK+1)]
        days.reverse() # Days Increasing from 7 days ago to 1 day ago

        for idx in range(len(days)):
            date = days[idx]
            date_str = date.strftime(DATETIME_STR_FORMAT)
            num_days_simulated = idx
            print(f'Day {idx} - {date_str}')

            # patron traffic for current day
            self.simulate_patron_traffic(patron_accounts, date, date_str) 
            self.simulate_restaurant_traffic(rest_accounts, date)
            
            if num_days_simulated >= 3:
                print('\tCalling manualAnalytics') #NOTE
                call_command('manualAnalytics', '-d', date_str)
        print('\n') #NOTE


    def simulate_today(self, today, patron_accounts, rest_accounts):
        today_str = today.strftime(DATETIME_STR_FORMAT)

        print('*'*50) #NOTE
        print("Simulating Today's Data") #NOTE
        print('*'*50 + '\n') #NOTE

        print(f'Today - {today_str}') #NOTE
        self.simulate_patron_traffic(patron_accounts, today, today_str)
        self.simulate_restaurant_traffic(rest_accounts, today)
        
        print('\tCalling manualAnalytics') #NOTE
        call_command('manualAnalytics', '-d', today_str)

        print('\tCalling manualTrends') #NOTE
        call_command('manualTrends', '-d', today_str)
    

    def simulate_patron_traffic(self, patron_accounts, date, date_str):
        print('\tSimulating Patron Traffic') #NOTE
        for account in patron_accounts:
            for _ in range(random.choices(LOGIN_COUNTS, LOGIN_WEIGHTS, k=1)[0]):
                LoginRecord.objects.create(user=account, date_stamp=date)

            num_searches = random.choices(SEARCH_COUNTS, SEARCH_WEIGHTS, k=1)[0]
            call_command('generatePatronTraffic', account.email, 
                         '-n', str(num_searches),
                         '-d', date_str,
                         '--no_report')
            
            print(f'\t\t{account.email} Logged In and Performed {num_searches} Search(es)') #NOTE
        print('\n') #NOTE


    def simulate_restaurant_traffic(self, rest_accounts, date):
        print('\tSimulating Restaurant Traffic') #NOTE
        for account in rest_accounts:
            for _ in range(random.choices(LOGIN_COUNTS, LOGIN_WEIGHTS, k=1)[0]):
                LoginRecord.objects.create(user=account, date_stamp=date)
            print(f'\t\t{account} Logged In') #NOTE
        print('\n') #NOTE


    def check_flags(self, options):
        if options['hard_reset']:
            self.hard_reset()
            self.stdout.write(self.style.SUCCESS(f"Hard Reset Completed!"))
            exit()

        if options['soft_reset']:
            self.soft_reset()
            self.stdout.write(self.style.SUCCESS(f"Soft Reset Completed!"))
            

    def hard_reset(self):

        # Delete Patron Traffic from the past 7 days
        today = timezone.now()
        lower_bound = today - timedelta(days=NUM_DAYS_BACK)
        self.clear_traffic(lower_bound)

        # Delete All Analytics and Trends
        clear_analytics.driver()    
        clear_trends.driver()

    
    def soft_reset(self):
        today = timezone.now()
        lower_bound = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=today.tzinfo)

        # Delete Patron Traffic, Analytics, and Trends from Today
        self.clear_traffic(lower_bound)
        clear_analytics.driver(lower_bound)    
        clear_trends.driver(lower_bound)


    def clear_traffic(self, lower_bound):
        PatronSearchHistory.objects.filter(search_datetime__gte=lower_bound).delete()
        Bookmark.objects.filter(bookmarked_datetime__gte=lower_bound).delete()
        MenuItemHistory.objects.filter(MenuItemHS_datetime__gte=lower_bound).delete()
        Reviews.objects.filter(review_datetime__gte=lower_bound).delete()

