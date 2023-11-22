from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.db.models import Avg
from datetime import datetime
from django.utils import timezone

import patron.models as pm
import restaurants.models as rm
from feedback.models import AppSatisfaction
from ..models import GlobalAnalytics, AppSatisfactionAnalytics

User = get_user_model()

def driver ():
    overall_data = overall_analysis()
    gender_data = gender_analysis()
    age_data = age_analysis()
    app_data = app_satisfaction_analysis()

    global_data = {**overall_data, **gender_data, **age_data}
    
    print(f'\nGlobal Analytics Object: {global_data}') #NOTE
    print(f'App Satisfaction Analytics: {app_data}') #NOTE

    # GlobalAnalytics.objects.create(**global_data)
    # AppSatisfactionAnalytics.objects.create(**app_data)

def overall_analysis():
    overall_data = {}

    overall_data['total_users'] = User.objects.all().count()
    overall_data['total_patrons'] = User.objects.filter(user_type='patron').count()
    overall_data['total_restaurants'] = User.objects.filter(user_type='patron').count()
    overall_data['total_menu_items'] = rm.MenuItem.objects.all().count()

    print(f"Overall Analysis:\n\tTotal Users: {overall_data['total_users']}"+ #NOTE
                          f"\n\tTotal Patrons: {overall_data['total_patrons']}"+ #NOTE
                          f"\n\tTotal Restaurants: {overall_data['total_restaurants']}"+ #NOTE
                          f"\n\tTotal Menu Items: {overall_data['total_menu_items']}\n") #NOTE
    
    return overall_data

def gender_analysis():
    gender_data = {}

    gender_data['total_males'] = pm.Patron.objects.filter(gender='Male').count()
    gender_data['total_females'] = pm.Patron.objects.filter(gender='Female').count()
    gender_data['total_other'] = pm.Patron.objects.filter(gender='Other').count()

    print(f"Gender Analysis:\n\tTotal Males: {gender_data['total_males']}"+ #NOTE
                         f"\n\tTotal Females: {gender_data['total_females']}"+ #NOTE
                         f"\n\tTotal Other: {gender_data['total_other']}\n") #NOTE
    
    return gender_data
    
def age_analysis():

    age_data = {}
    current_day = date.today()
    bound_info = [(18, 24, 'users_18_24'), (25, 34, 'users_25_34'), (35, 44, 'users_35_44'),
                  (45, 54, 'users_45_54'), (55, 64, 'users_55_64'), (65, -1, 'users_65_and_up')]

    for lower, upper, idx in bound_info:
        lower_day = current_day - timedelta(days=365.25*lower)
        if upper != -1:
            upper_day = current_day - timedelta(days=365.25*(upper+1)-1)
    
            age_data[idx] = pm.Patron.objects.filter(
                dob__gte=upper_day,
                dob__lte=lower_day
            ).count()
        else:
            age_data[idx] = pm.Patron.objects.filter(
                dob__lte=lower_day
            ).count()

    print(f'Age Analysis:') #NOTE
    for lower, upper, idx in bound_info: #NOTE
        print(f'\tAges {lower}-{upper}: {age_data[idx]}') #NOTE

    return age_data


def app_satisfaction_analysis():
    app_data = {}

    # try:
    #     latest_datestamp = AppSatisfactionAnalytics.objects.latest('date_stamp').date_stamp
    # except AppSatisfactionAnalytics.DoesNotExist:
    #     latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

    ratings = AppSatisfaction.objects.all()

    app_data['number_of_rating_total'] = ratings.count()
    # app_data['number_of_rating_since'] = ratings.filter(review_datetime__gt=latest_datestamp).count() #TODO Remove
    app_data['number_of_rating_since'] = 0 #TODO Remove
    app_data['average_rating'] = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    return app_data
    