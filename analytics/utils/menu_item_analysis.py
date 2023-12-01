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

# Number of searches Menu Items were excluded from (total since)

def driver():

    item_data, current_datestamp = item_analysis()

    item_data = item_exclusion_analysis(item_data)

    for entry in item_data:
        # print(f'{current_datestamp} | {entry}') #NOTE
        obj = MenuItemPerformanceAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)

        update_menu_item(entry)
    print('\n')

def item_analysis(items, bookmark_set, history_set, review_set):
    
    try:
        latest_datestamp = MenuItemPerformanceAnalytics.objects.latest('date_stamp').date_stamp
    except MenuItemPerformanceAnalytics.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    
    item_data = []

    items = rm.MenuItem.objects.all().order_by('id')
    bookmark_set = pm.Bookmark.objects.filter(bookmarked_datetime__gt=latest_datestamp)
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    review_set = Reviews.objects.all()
    current_datestamp = timezone.now()

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

    return item_data, current_datestamp


def update_menu_item(entry):
    item_instance = entry['menuItem_id']
    
    item_instance.number_of_rating = entry['number_of_ratings']
    item_instance.average_rating = entry['average_rating']
    item_instance.save()


def item_exclusion_analysis(item_data):

    TAG_TYPES = [('allergy', rm.AllergyTag, AllergyTagExclusionRecord), 
                 ('ingredients', rm.IngredientTag, IngredientTagExclusionRecord), 
                 ('restrictions', rm.RestrictionTag, RestrictionTagExclusionRecord),
                 ('taste', rm.TasteTag, TasteTagExclusionRecord)]
    
    INDEXES = ['first', 'second', 'third']
    
    analytic_sets = {tag_type: AnalyticsModel.objects.all() for tag_type, _, AnalyticsModel in TAG_TYPES}
    overall_set = OverallExclusionRecord.objects.all()

    for entry in item_data:
        menu_item = entry['menuItem_id']

        # Overall Exclusion
        entry['exclusion_count'] = overall_set.get(menu_item=menu_item).exclusion_count

        for tag_type, *_ in TAG_TYPES:
            top_3 = list(analytic_sets[tag_type].filter(
                menu_item=menu_item
            ).order_by('-exclusion_count')[:3])

            entry[f'top_3_{tag_type}'] = {
                INDEXES[idx]: {
                    'title':record.tag.title,
                    'count':record.exclusion_count
                } for idx, record in enumerate(top_3)
            }

    return item_data



# # Store exclusion
    # for entry in item_data:
    #     menu_item = entry['menuItem_id']

    #     #Overall Exclusion
    #     entry['exclusion_count'] = overall_exclusions[f'{menu_item.id}'].count

    #     for tag_type, *_ in TAG_TYPES:
    #         tag_counts = tag_exclusions[tag_type][f'{menu_item.id}']
    #         sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    #         top_3 = sorted_tags[:3]
            
    #         idx, tag_dict = 1, {}
    #         for tag_id, count in top_3:
    #             tag_dict[f'{idx}'] = {
    #                 'title':tag_sets[tag_type].get(id=tag_id).title,
    #                 'count':count
    #             }
    #         entry[f'top_3_{tag_type}'] = tag_dict

    # return item_data
                
