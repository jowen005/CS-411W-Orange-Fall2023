from django.contrib.auth import get_user_model
from datetime import date, timedelta

import patron.models as pm
import restaurants.models as rm

User = get_user_model()

def driver ():
    overall_analysis()
    gender_analysis()
    age_analysis()


def overall_analysis():
    total_users = User.objects.all().count()
    total_patrons = User.objects.filter(user_type='patron').count()
    total_restaurants = User.objects.filter(user_type='patron').count()
    total_menu_items = rm.MenuItem.objects.all().count()

    print(f'Overall Analysis:\n\tTotal Users: {total_users}'+ #NOTE
                          f'\n\tTotal Patrons: {total_patrons}'+ #NOTE
                          f'\n\tTotal Restaurants: {total_restaurants}'+ #NOTE
                          f'\n\tTotal Menu Items: {total_menu_items}\n') #NOTE

def gender_analysis():
    total_males = pm.Patron.objects.filter(gender='Male').count()
    total_females = pm.Patron.objects.filter(gender='Female').count()
    total_other = pm.Patron.objects.filter(gender='Other').count()

    print(f'Gender Analysis:\n\tTotal Males: {total_males}'+ #NOTE
                         f'\n\tTotal Females: {total_females}'+ #NOTE
                         f'\n\tTotal Other: {total_other}\n') #NOTE
    
def age_analysis():
    lower_bounds = [18, 25, 35, 45, 55, 65]
    upper_bounds = [24, 34, 44, 54, 64, -1]
    results = [0 for _ in range(len(lower_bounds))]
    current_day = date.today()

    # print(f'{pm.Patron.objects.all().values_list("dob", flat=True)}')

    for idx in range(len(lower_bounds)):
        lower_day = current_day - timedelta(days=365.25*lower_bounds[idx])
        if upper_bounds[idx] != -1:
            upper_day = current_day - timedelta(days=365.25*(upper_bounds[idx]+1)-1)
    
            results[idx] = pm.Patron.objects.filter(
                dob__gte=upper_day,
                dob__lte=lower_day
            ).count()
        else:
            results[idx] = pm.Patron.objects.filter(
                dob__lte=lower_day
            ).count()

    print(f'Age Analysis:') #NOTE
    for idx in range(len(lower_bounds)-1):  #NOTE
        print(f'\tAges {lower_bounds[idx]}-{upper_bounds[idx]}: {results[idx]}')  #NOTE
    print(f'\tAge {lower_bounds[-1]} and up: {results[-1]}\n') #NOTE