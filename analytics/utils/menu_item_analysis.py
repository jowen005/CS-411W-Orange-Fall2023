from datetime import datetime
from django.utils import timezone
from django.db.models import Avg

import patron.models as pm
import restaurants.models as rm
from feedback.models import Reviews
from ..models import MenuItemPerformanceAnalytics

# Number of searches Menu Items were excluded from (total since)

def driver():

    item_data, current_datestamp = item_analysis()

    for entry in item_data:
        # print(f'{current_datestamp} | {entry}') #NOTE
        obj = MenuItemPerformanceAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)

        item_instance = entry['menuItem_id']
    
        item_instance.number_of_rating = entry['number_of_ratings']
        item_instance.average_rating = entry['average_rating']
        item_instance.save()
    print('\n')

def item_analysis():
    items = rm.MenuItem.objects.all().order_by('id')
    item_data = []

    try:
        latest_datestamp = MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
    except MenuItemPerformanceAnalytics.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

    bookmark_set = pm.Bookmark.objects.filter(bookmarked_datetime__gt=latest_datestamp)
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    review_set = Reviews.objects.all()
    current_datestamp = timezone.now()

    for item in items:
        data = {}

        data['menuItem_id'] = item
        data['number_of_added_to_bookmark'] = bookmark_set.filter(
            menu_item__id=item.id,
        ).count()
        data['number_of_added_to_History'] = history_set.filter(
            menu_item__id=item.id,
        ).count()

        ratings = review_set.filter(menu_item__id=item.id)
        data['number_of_ratings'] = ratings.count()
        data['average_rating'] = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

        item_data.append(data)

    return item_data, current_datestamp
