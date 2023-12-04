from django.utils import timezone
from datetime import datetime, timedelta
from dataclasses import dataclass
from django.core.serializers import serialize
import sys
import time

import restaurants.models as rm
import patron.models as pm
from ..models import LocalRestaurantAnalytics
from ..models import (AllergyTagExclusionRecord, IngredientTagExclusionRecord,
                      RestrictionTagExclusionRecord, TasteTagExclusionRecord,
                      OverallExclusionRecord)

def driver():
    restaurant_data, current_datestamp = restaurant_analysis()
    print(restaurant_data)
    print(current_datestamp)


def restaurant_analysis():

    # Past 3 Days (Data Overlap)
    latest_datestamp = timezone.now() - timedelta(days=3)

    TAG_TYPES = [('allergy', rm.AllergyTag, LocalRestaurantAnalytics), 
                 ('ingredients', rm.IngredientTag, LocalRestaurantAnalytics), 
                 ('restrictions', rm.RestrictionTag, LocalRestaurantAnalytics),
                 ('taste', rm.TasteTag, LocalRestaurantAnalytics),
                 ('cook_style', rm.CookStyleTag, LocalRestaurantAnalytics)]

    # List storing the restaurant fields
    restaurant_data = []


    restaurants = rm.Restaurant.objects.all()
    # List storing all fields for an entry in the LocalRestaurantAnalytics Model
    #restaurant_data = ['total_items_added_to_histories', '']


    items = rm.MenuItem.objects.all().order_by('id')
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    searches = pm.PatronSearchHistory.objects.filter(search_datetime__gte=latest_datestamp)
    current_datestamp = timezone.now()

    # Get all the fields for each restaurant
    for restaurant in restaurants:
        data = {}
        data['restaurant_id'] = restaurant
        data['total_items_added_to_histories'] = total_added_to_histories(restaurant, latest_datestamp)

        restaurant_data.append(data)

    
    #data = {}
    #for restaurant in restaurants:
       

    # Go through all menu items in each history and count which ones have the same restaurant id as 'restaurant'
    #for history in history_set:
        # Number of items from restaurant in that history, add each iteration
     #   pass
    # Will have the number added to histories for each restaurant

        # The below does not work (I don't think)

        # data['total_items_added_to_histories'] = history_set.filter(
        #     menu_restaurant_id = restaurant.id
        # ).count()

        # restaurant_data.append(data)

        # For each tag which one excludes the most items (use similar algorithm to exclusion analysis)

    return restaurant_data, current_datestamp

    

# Function for finding total items from a restaurant added to histories (the restaurant and latest datestamp is supplied)
def total_added_to_histories(rest, latest_datestamp):
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    # Only iterate through the items from the specified restaurant
    items = rm.MenuItem.objects.filter(restaurant = rest)
    # Get all the items that have been added to patrons histories
    items_in_histories = []
    for history in history_set:
        items_in_histories.append(history.menu_item)
    
    # Check every item to see if it is in a patron's history (or multiple patrons)
    total_items_added_to_histories = 0

    for item in items:
        for h_item in items_in_histories:
            if item == h_item:
                total_items_added_to_histories += 1

       # history_count = history.menu_item.filter(restaurant = rest).count()
        #total_items_added_to_histories += history_count
            # restaurant_items = items.filter(restaurant=rest)
            # for item in restaurant_items:
    # for history in history_set:
    #     for item in items:
    #         if history.menu_item.id = item.id:


        # Number of items from restaurant in that history, add each iteration
    # Will have the number added to histories for the restaurant
    return total_items_added_to_histories
    #print(total_items_added_to_histories)
    