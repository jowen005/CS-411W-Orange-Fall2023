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
    # print(restaurant_data)
    # print(current_datestamp)

    # Save the new analytic records in the model
    # for entry in restaurant_data:
    #     obj = LocalRestaurantAnalytics.objects.create(**entry, date_stamp=current_datestamp)
    #     print(obj)
    #     print('\n')


def restaurant_analysis():

    # Past 3 Days (Data Overlap)
    latest_datestamp = timezone.now() - timedelta(days=3)

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
        data['top_three_items'] = top_3_items_analysis(restaurant)
        data['total_items_added_to_histories'] = total_added_to_histories(restaurant, latest_datestamp)
        data['allergies_tags_most_eliminations'], data['ingredient_tags_most_eliminations'], data['restriction_tags_most_eliminations'], data['taste_tags_most_eliminations'] = tag_eliminations_analysis(restaurant, latest_datestamp)
        #tag_eliminations_analysis(restaurant, latest_datestamp)

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
    #print(items_in_histories)

def top_3_items_analysis(rest):
    INDEXES = ['first', 'second', 'third']
    items = rm.MenuItem.objects.filter(restaurant = rest)
    top_3_scores = []
    top_3_items = []
    performance_scores = []
    
    # Calculate the performance scores
    for item in items:
        performance = (item.average_rating * item.number_of_rating)
        performance_scores.append(performance)
    
    # Sort the scores in ascending order
    performance_scores.sort(reverse=True)
    # Get the top 3 scores
    top_3_scores = performance_scores[:3]

    # Get the items associated with the top 3 scores (the first 3 reached will be counted, ties do not matter)
    # This is why the list is being sorted backwards, so items added recently have advantage
    counter = 0
    #counter = 'first'
    for p_score in top_3_scores:
        for item in reversed(items):
            if counter < 3:
                if p_score == item.average_rating * item.number_of_rating:
                    item = {
                        INDEXES[counter]: {
                        'title': item.item_name,
                        'score': p_score
                        }
                    }
                    counter += 1
                    top_3_items.append(item)
                    # if counter == 'first':
                    #     counter = 'second'
                    # else:
                    #     counter = 'third'
    
    return top_3_items

def tag_eliminations_analysis(rest, latest_datestamp):
    # TAG_TYPES = [('allergy', rm.AllergyTag, LocalRestaurantAnalytics), 
    #              ('ingredients', rm.IngredientTag, LocalRestaurantAnalytics), 
    #              ('restrictions', rm.RestrictionTag, LocalRestaurantAnalytics),
    #              ('taste', rm.TasteTag, LocalRestaurantAnalytics)]
    
    items = rm.MenuItem.objects.filter(restaurant = rest)
    searches = pm.PatronSearchHistory.objects.filter(search_datetime__gte=latest_datestamp)

    #tag_sets = {tag_type: TagModel.objects.all().order_by('id') for tag_type, TagModel, *_ in TAG_TYPES}

    # tag_exclusions = {
    #     tag_type:{
    #         tag: {
    #             exclusion_count
    #         }
    #     }
    # }

    # tag_exclusions = {
    #     tag_type: {
    #         f'{item.id}': {
    #             f'{tag.id}':0 for tag in tag_sets[tag_type]}
    #         for item in items} 
    #     for tag_type, *_ in TAG_TYPES
    # }
    total_allergy_counts = []
    total_allergy = []

    total_ingredient_counts = []
    total_ingredient = []

    total_restriction_counts = []
    total_restrictions = []

    total_taste_counts = []
    total_taste = []
    
    for search in searches:
        # Excluded if item has allergy tag
        for allergy in search.allergy_tags.all():
            excluded_items = items.filter(menu_allergy_tag=allergy)

            if allergy in total_allergy:
                for a in range(len(total_allergy)):
                    if allergy == total_allergy[a]:
                        for e in excluded_items:
                            total_allergy_counts[a] += 1
            else:
                allergy_counts = 0
                for e in excluded_items:
                    allergy_counts += 1
                total_allergy_counts.append(allergy_counts)
                total_allergy.append(allergy)

        # for allergy in search.allergy_tags.all():
        #     excluded_items = items.filter(menu_allergy_tag=allergy)
        #     allergy_count = 0
        #     for item in excluded_items:
        #         tag_exclusions['allergy'][f'{item.id}'][f'{allergy.id}'] += 1
        
        # Excluded if item has any of the disliked ingredients (record tags that led to it getting excluded)
        for ingredient in search.disliked_ingredients.all():
            excluded_items = items.filter(ingredients_tag=ingredient)

            if ingredient in total_ingredient:
                for j in range(len(total_ingredient)):
                    if ingredient == total_ingredient[j]:
                        for e in excluded_items:
                            total_ingredient_counts[j] += 1
            else:
                ingredient_counts = 0
                for e in excluded_items:
                    ingredient_counts += 1
                total_ingredient_counts.append(ingredient_counts)
                total_ingredient.append(ingredient)

        # for ingredient in search.disliked_ingredients.all():
        #     excluded_items = items.filter(ingredients_tag=ingredient)
        #     disliked_ingredient_count = 0
        #     for item in excluded_items:
        #         tag_exclusions['ingredients'][f'{item.id}'][f'{ingredient.id}'] += 1

        
        #Excluded if item does not have restriction tag
        for restriction in search.dietary_restriction_tags.all():
            excluded_items = items.exclude(menu_restriction_tag=restriction)
            #restriction_count = 0
            if restriction in total_restrictions:
                for i in range(len(total_restrictions)):
                    if restriction == total_restrictions[i]:
                        for e in excluded_items:
                            total_restriction_counts[i] += 1
            else:
                # print('a')
                restrictions_counts = 0
                for e in excluded_items:
                    restrictions_counts += 1
                    # print('a')
                total_restriction_counts.append(restrictions_counts)
                total_restrictions.append(restriction)
                    
        #     for item in excluded_items:
        #         restrictions_counts += 1
        #     total_restriction_counts[i] = 
        #         #tag_exclusions['restrictions'][f'{item.id}'][f'{restriction.id}'] += 1
        # for restrict in restriction_count:
        #     if total_restrictions[i] == restrictions[i]:
        #         restrictions[i]


        # Excluded if item does not have any of the taste tags (record tags that led to it getting excluded)
        excluded_items = items.exclude(taste_tags__in=search.patron_taste_tags.all())
        for e in excluded_items:
            for taste in search.patron_taste_tags.all():
                if taste in total_taste:
                    for t in range(len(total_taste)):
                        if taste == total_taste[t]:
                            total_taste_counts[t] += 1
                else:
                    taste_counts = 0
                    taste_counts += 1
                total_taste_counts.append(taste_counts)
                total_taste.append(taste) 

        # excluded_items = items.exclude(taste_tags__in=search.patron_taste_tags.all())
        # for item in excluded_items:
        #     for taste in search.patron_taste_tags.all():
        #         tag_exclusions['taste'][f'{item.id}'][f'{taste.id}'] += 1
        
        
    # Get the max of each total count and the correspoding tag
    # Allergy
    for i in range(len(total_allergy_counts)):
       if total_allergy_counts[i] == max(total_allergy_counts):
           max_allergy_eliminations = total_allergy_counts[i]
           max_allergy_tag = total_allergy[i]
    
    # Ingredient
    for i in range(len(total_ingredient_counts)):
        if total_ingredient_counts[i] == max(total_ingredient_counts):
            max_ingredient_eliminations = total_ingredient_counts[i]
            max_ingredient_tag = total_ingredient[i]

    # Restriction
    for i in range(len(total_restriction_counts)):
        if total_restriction_counts[i] == max(total_restriction_counts):
            max_restriction_eliminations = total_restriction_counts[i]
            max_restriction_tag = total_restrictions[i]

    # Taste
    for i in range(len(total_taste_counts)):
        if total_taste_counts[i] == max(total_taste_counts):
            max_taste_eliminations = total_taste_counts[i]
            max_taste_tag = total_taste[i]

    # Crete the JSONs for each tag
    allergies_tags_most_eliminations = {
        'allergy tag': max_allergy_tag,
        'eliminations': max_allergy_eliminations
    }

    ingredient_tags_most_eliminations = {
        'ingredient tag': max_ingredient_tag,
        'eliminations': max_ingredient_eliminations
    }

    restriction_tags_most_eliminations = {
        'restriction tag': max_restriction_tag,
        'eliminations': max_restriction_eliminations
    }

    taste_tags_most_eliminations = {
        'taste tag': max_taste_tag,
        'eliminations': max_taste_eliminations
    }

    return allergies_tags_most_eliminations, ingredient_tags_most_eliminations, restriction_tags_most_eliminations, taste_tags_most_eliminations
    
