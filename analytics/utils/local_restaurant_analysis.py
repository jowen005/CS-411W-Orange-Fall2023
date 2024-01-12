from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

import restaurants.models as rm
import patron.models as pm
from ..models import LocalRestaurantAnalytics
from ..models import (AllergyTagExclusionRecord, IngredientTagExclusionRecord,
                      RestrictionTagExclusionRecord, TasteTagExclusionRecord)

def driver(sim_datetime):
    restaurant_data, current_datestamp = restaurant_analysis(sim_datetime)

    # Save the new analytic records in the model
    for entry in restaurant_data:
        # print(entry)
        obj = LocalRestaurantAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)
        print('\n')


def restaurant_analysis(sim_datetime):

    if sim_datetime is None:
        current_datestamp = timezone.now()
    else:
        current_datestamp = sim_datetime

    # Past 3 Days (Data Overlap)
    latest_datestamp = current_datestamp - timedelta(days=3)

    # List storing the restaurant fields
    restaurant_data = []


    restaurants = rm.Restaurant.objects.all()

    # Get all the fields for each restaurant
    for restaurant in restaurants:
        data = {}
        data['restaurant_id'] = restaurant
        data['top_three_items'] = top_3_items_analysis(restaurant)
        data['total_items_added_to_histories'] = total_added_to_histories(restaurant, latest_datestamp)
        data['allergies_tags_most_eliminations'] = top_tag_analysis(restaurant, AllergyTagExclusionRecord)
        data['ingredient_tags_most_eliminations'] = top_tag_analysis(restaurant, IngredientTagExclusionRecord)
        data['restriction_tags_most_eliminations'] = top_tag_analysis(restaurant, RestrictionTagExclusionRecord)
        data['taste_tags_most_eliminations'] = top_tag_analysis(restaurant, TasteTagExclusionRecord)

        restaurant_data.append(data)

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


        # Number of items from restaurant in that history, add each iteration
    # Will have the number added to histories for the restaurant
    return total_items_added_to_histories
    #print(items_in_histories)

def top_3_items_analysis(rest):
    INDEXES = ['first', 'second', 'third']
    items = rm.MenuItem.objects.filter(restaurant = rest)
    top_3_scores = []
    top_3_items = {}
    performance_scores = []
    
    # Calculate the performance scores
    for item in items:
        performance = float(item.average_rating * item.number_of_rating)
        performance_scores.append(performance)
    
    # Sort the scores in ascending order
    performance_scores.sort(reverse=True)
    # Get the top 3 scores
    top_3_scores = performance_scores[:3]

    # Get the items associated with the top 3 scores (the first 3 reached will be counted, ties do not matter)
    # This is why the list is being sorted backwards, so items added recently have advantage
    counter = 0
    for p_score in top_3_scores:
        for item in reversed(items):
            if counter < 3:
                if p_score == item.average_rating * item.number_of_rating:
                    
                    top_3_items[INDEXES[counter]] = {
                        'title': item.item_name,
                        'score': p_score
                    }
                    counter += 1
    
    return top_3_items

def top_tag_analysis(rest, ExclusionRecord):
    queryset = ExclusionRecord.objects.filter(
        menu_item__restaurant=rest
    ).values('tag__title').annotate(total=Sum('exclusion_count')).order_by('-total')

    top_tag = queryset.first()

    if top_tag is not None:
        top_tag_data = {
            "tag": top_tag['tag__title'],
            "eliminations": top_tag['total']
        }
    else:
        top_tag_data = "N/A"

    return top_tag_data

