from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone

import patron.models as pm
import restaurants.models as rm
from feedback.models import AppSatisfaction
from ..models import GlobalAnalytics

User = get_user_model()

def driver (sim_datetime):
    if sim_datetime is None:
        current_datestamp = timezone.now()
    else:
        current_datestamp = sim_datetime

    overall_data = overall_analysis()
    gender_data = gender_analysis()
    age_data = age_analysis()

    global_data = {**overall_data, **gender_data, **age_data}
    
    # print(f'\nGlobal Analytics Object: {global_data}') #NOTE

    obj = GlobalAnalytics.objects.create(**global_data, date_stamp=current_datestamp)
    print(f'{obj}\n')

def overall_analysis():
    overall_data = {}
    user_set = User.objects.all()

    overall_data['total_users'] = user_set.exclude(user_type='admin').count()
    overall_data['total_patrons'] = user_set.filter(user_type='patron').count()
    overall_data['total_restaurants'] = user_set.filter(user_type='restaurant').count()
    overall_data['total_menu_items'] = rm.MenuItem.objects.all().count()

    # print(f"Overall Analysis:\n\tTotal Users: {overall_data['total_users']}"+ #NOTE
                        #   f"\n\tTotal Patrons: {overall_data['total_patrons']}"+ #NOTE
                        #   f"\n\tTotal Restaurants: {overall_data['total_restaurants']}"+ #NOTE
                        #   f"\n\tTotal Menu Items: {overall_data['total_menu_items']}\n") #NOTE
    
    return overall_data

def gender_analysis():
    gender_data = {}

    patron_set = pm.Patron.objects.all()
    gender_data['total_males'] = patron_set.filter(gender='Male').count()
    gender_data['total_females'] = patron_set.filter(gender='Female').count()
    gender_data['total_other'] = patron_set.filter(gender='Other').count()

    # print(f"Gender Analysis:\n\tTotal Males: {gender_data['total_males']}"+ #NOTE
                        #  f"\n\tTotal Females: {gender_data['total_females']}"+ #NOTE
                        #  f"\n\tTotal Other: {gender_data['total_other']}\n") #NOTE
    
    return gender_data
    
def age_analysis():

    age_data = {}
    patron_set = pm.Patron.objects.all()
    current_day = date.today()
    bound_info = [(18, 24, 'users_18_24'), (25, 34, 'users_25_34'), (35, 44, 'users_35_44'),
                  (45, 54, 'users_45_54'), (55, 64, 'users_55_64'), (65, -1, 'users_65_and_up')]

    for lower, upper, idx in bound_info:
        lower_day = current_day - timedelta(days=365.25*lower)
        if upper != -1:
            upper_day = current_day - timedelta(days=365.25*(upper+1)-1)
    
            age_data[idx] = patron_set.filter(
                dob__gte=upper_day,
                dob__lte=lower_day
            ).count()
        else:
            age_data[idx] = patron_set.filter(
                dob__lte=lower_day
            ).count()

    # print(f'Age Analysis:') #NOTE
    # for lower, upper, idx in bound_info: #NOTE
        # print(f'\tAges {lower}-{upper}: {age_data[idx]}') #NOTE

    return age_data
