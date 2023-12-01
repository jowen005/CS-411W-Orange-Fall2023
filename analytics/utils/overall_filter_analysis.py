from datetime import datetime
from django.utils import timezone

from ..models import (RestrictionTagAnalytics, AllergiesTagAnalytics, 
                      TasteTagAnalytics, IngredientTagAnalytics, 
                      CookStyleAnalytics, CalorieAnalytics)
from ..models import OverallFilterAnalytics
import restaurants.models as rm


def driver():
    FILTER_TYPES = [('calories', CalorieAnalytics, ),
                    ('cookstyletag', CookStyleAnalytics),
                    ('allergytag', AllergiesTagAnalytics), 
                    ('ingredienttag', IngredientTagAnalytics), 
                    ('restrictiontag', RestrictionTagAnalytics),
                    ('tastetag', TasteTagAnalytics)]
    
    overall_analytics = analysis(FILTER_TYPES)
    current_datestamp = timezone.now()

    for entry in overall_analytics:
        # print(entry)
        obj = OverallFilterAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)
    print('\n')

    
def analysis(FILTER_TYPES):
    INDEXES = ['first', 'second', 'third']
    overall_analytics = []
    
    for filter, AnalyticsModel in FILTER_TYPES:
        try:
            latest_datestamp = AnalyticsModel.objects.latest('date_stamp').date_stamp
        except AnalyticsModel.DoesNotExist:
            print(f'There are No Analytics for {filter}\n')
            return

        analytic_set = AnalyticsModel.objects.filter(date_stamp=latest_datestamp)
        result_data = {}

        result_data['filter_type'] = filter

        if filter == 'calories':
            inclusions = list(analytic_set.order_by('-number_of_searches')[:3])
            result_data['top_3_inclusions'] = {
                INDEXES[idx]: {
                    'title':record.get_calorie_level_display(),
                    'count':record.number_of_searches
                } for idx, record in enumerate(inclusions)
            }

            added = list(analytic_set.order_by('-number_of_items_added_HIS')[:3])
            result_data['top_3_added'] = {
                INDEXES[idx]: {
                    'title':record.get_calorie_level_display(),
                    'count':record.number_of_items_added_HIS
                } for idx, record in enumerate(added)
            }

        else:
            inclusions = list(analytic_set.order_by('-number_of_search')[:3])
            result_data['top_3_inclusions'] = {
                INDEXES[idx]: {
                    'title':record.tag_id.title,
                    'count':record.number_of_search
                } for idx, record in enumerate(inclusions)
            }

            added = list(analytic_set.order_by('-number_of_HIS')[:3])
            result_data['top_3_added'] = {
                INDEXES[idx]: {
                    'title':record.tag_id.title,
                    'count':record.number_of_HIS
                } for idx, record in enumerate(added)
            }

            if filter != 'cookstyletag':
                exclusions = list(analytic_set.order_by('-exclusion_count')[:3])
                result_data['top_3_exclusions'] = {
                    INDEXES[idx]: {
                        'title':record.tag_id.title,
                        'count':record.exclusion_count
                    } for idx, record in enumerate(exclusions)
                }

        overall_analytics.append(result_data)
    
    return overall_analytics

    