from datetime import datetime
from django.utils import timezone
from django.db.models import Avg

import patron.models as pm
import restaurants.models as rm
from feedback.models import Reviews
from ..models import MenuItemPerformanceAnalytics

# Number of searches Menu Items were excluded from (total since)

def driver():
    item_data = item_analysis()

    menu_items = rm.MenuItem.objects.all()

    for entry in item_data:
        print(f'{entry}') #NOTE
        # obj = MenuItemPerformanceAnalytics.objects.create(**entry)
        # print(obj)
        item_instance = menu_items.get(id=entry['menuItem_id'].id)
        
        if item_instance:
            print(f'{item_instance}\n') #NOTE
            item_instance.number_of_rating = entry['number_of_ratings']
            item_instance.average_rating = entry['average_rating']
            item_instance.save()
        


def item_analysis():
    items = rm.MenuItem.objects.all().order_by('id')
    item_data = []

    try:
        latest_datestamp = MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
    except MenuItemPerformanceAnalytics.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

    for item in items:
        data = {}

        data['menuItem_id'] = item
        data['number_of_added_to_bookmark'] = pm.Bookmark.objects.filter(
            menu_item__id=item.id,
            bookmarked_datetime__gt=latest_datestamp
        ).count()
        data['number_of_added_to_History'] = pm.MenuItemHistory.objects.filter(
            menu_item__id=item.id,
            MenuItemHS_datetime__gt=latest_datestamp
        ).count()

        ratings = Reviews.objects.filter(menu_item__id=item.id)
        data['number_of_ratings'] = ratings.count()
        data['average_rating'] = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

        item_data.append(data)

    return item_data
