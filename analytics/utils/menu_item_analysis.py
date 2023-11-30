from datetime import datetime
from django.utils import timezone
from django.db.models import Avg

import patron.models as pm
import restaurants.models as rm
from feedback.models import Reviews
from ..models import MenuItemPerformanceAnalytics
from ..models import (AllergyTagExclusionRecord, IngredientTagExclusionRecord,
                      RestrictionTagExclusionRecord, TasteTagExclusionRecord,
                      OverallExclusionRecord)

import tag_exclusion

# Number of searches Menu Items were excluded from (total since)

def driver():

    try:
        latest_datestamp = MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
    except MenuItemPerformanceAnalytics.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

    menu_items = rm.MenuItem.objects.all().order_by('id')
    searches = pm.PatronSearchHistory.filter(search_datetime__gte=latest_datestamp)
    bookmark_set = pm.Bookmark.objects.filter(bookmarked_datetime__gt=latest_datestamp)
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    review_set = Reviews.objects.all()
    current_datestamp = timezone.now()

    item_data = item_analysis(menu_items, bookmark_set, history_set, review_set)
    item_data = tag_exclusion.driver(item_data, menu_items, searches)

    for entry in item_data:
        # print(f'{current_datestamp} | {entry}') #NOTE
        obj = MenuItemPerformanceAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)

        update_menu_item(entry)
    print('\n')


def update_menu_item(entry):
    item_instance = entry['menuItem_id']
    
    item_instance.number_of_rating = entry['number_of_ratings']
    item_instance.average_rating = entry['average_rating']
    item_instance.save()


def item_analysis(items, bookmark_set, history_set, review_set):
    # items = rm.MenuItem.objects.all().order_by('id') #filter(discontinued=False)
    item_data = []

    

    # bookmark_set = pm.Bookmark.objects.filter(bookmarked_datetime__gt=latest_datestamp)
    # history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    # review_set = Reviews.objects.all()
    # current_datestamp = timezone.now()

    for item in items:
        data = {}

        data['menuItem_id'] = item
        data['number_of_added_to_bookmark'] = bookmark_set.filter(
            menu_item__id=item.id,
        ).count() #TODO: Remove
        data['number_of_added_to_History'] = history_set.filter(
            menu_item__id=item.id,
        ).count()

        ratings = review_set.filter(menu_item__id=item.id)
        data['number_of_ratings'] = ratings.count()
        data['average_rating'] = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

        item_data.append(data)

    return item_data
