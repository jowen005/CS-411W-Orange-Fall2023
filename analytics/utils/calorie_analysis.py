from datetime import timedelta
from django.utils import timezone

import patron.models as pm
import restaurants.models as rm
from ..models import CalorieAnalytics


NUM_OF_CAL_LEVELS = 11


def driver(sim_datetime):
    calorie_data, current_datestamp = calorie_analysis(sim_datetime)
        
    for entry in calorie_data:
        # print(entry) #DEBUG
        obj = CalorieAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)
    print('\n')


def calorie_analysis(sim_datetime):
    
    if sim_datetime is None:
        current_datestamp = timezone.now()
    else:
        current_datestamp = sim_datetime

    # Past 3 Days (Data Overlap)
    latest_datestamp = current_datestamp - timedelta(days=3)

    calorie_data = [{} for _ in range(NUM_OF_CAL_LEVELS)]

    patron_set = pm.Patron.objects.all()
    item_set = rm.MenuItem.objects.all()
    search_set = pm.PatronSearchHistory.objects.filter(search_datetime__gt=latest_datestamp)
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)

    for idx in range(NUM_OF_CAL_LEVELS):
        current_level = idx + 1

        calorie_data[idx]['calorie_level'] = current_level

        # Number of profiles within range (total)
        calorie_data[idx]["number_of_profiles"] = patron_set.filter(
            calorie_level=current_level
        ).count()

        # Number of menu items within range (total)
        calorie_data[idx]["number_of_menuItems"] = item_set.filter(
            calorie_level=current_level
        ).count()

        # Number of searches within range (total since)
        calorie_data[idx]["number_of_searches"] = search_set.filter(
            calorie_level=current_level
        ).count()

        # Number of items added to history within range (total since)
        calorie_data[idx]["number_of_items_added_HIS"] = history_set.filter(
            menu_item__calorie_level=current_level
        ).count()

    # for idx in range(NUM_OF_CAL_LEVELS): #DEBUG
        # calorie_level = f'{idx*200} - {idx*200+199}' #DEBUG
        # print(f'{calorie_level}:\n\tProfiles: {calorie_data[idx]["number_of_profiles"]}\n' + #DEBUG
                                # f'\tMenu Items: {calorie_data[idx]["number_of_menuItems"]}\n' + #DEBUG
                                # f'\tSearches: {calorie_data[idx]["number_of_searches"]}\n' + #DEBUG
                                # f'\tHistory: {calorie_data[idx]["number_of_items_added_HIS"]}\n') #DEBUG
        
    return calorie_data, current_datestamp

