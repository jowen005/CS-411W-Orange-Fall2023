from django.utils import timezone
from django.core.serializers import serialize
import sys
from dataclasses import dataclass

from restaurants.models import (RestrictionTag, AllergyTag, IngredientTag, TasteTag, CookStyleTag)
from analytics.models import (RestrictionTagAnalytics, AllergiesTagAnalytics,
                              IngredientTagAnalytics, TasteTagAnalytics, 
                              CookStyleAnalytics, CalorieAnalytics)
from ..models import (RestrictionTagTrends, AllergyTagTrends,
                      IngredientTagTrends, TasteTagTrends, 
                      CookStyleTagTrends, CalorieTrends)
from . import trends


# (AnalyticsModel, TrendsModel, analytic_search_attr, analytic_history_attr)
FILTER_MODELS = [(RestrictionTag, RestrictionTagAnalytics, RestrictionTagTrends,
                        'number_of_search', 'number_of_HIS'),
                 (AllergyTag, AllergiesTagAnalytics, AllergyTagTrends,
                        'number_of_search', 'number_of_HIS'),
                 (IngredientTag, IngredientTagAnalytics, IngredientTagTrends, 
                        'number_of_search', 'number_of_HIS'),
                 (TasteTag, TasteTagAnalytics, TasteTagTrends, 
                        'number_of_search', 'number_of_HIS'),
                 (CookStyleTag, CookStyleAnalytics, CookStyleTagTrends, 
                        'number_of_search', 'number_of_HIS'),
                 (None, CalorieAnalytics, CalorieTrends, 
                        'number_of_searches', 'number_of_items_added_HIS')]


def driver(sim_datetime):

    for TagModel, AnalyticsModel, TrendsModel, search_attr, history_attr in FILTER_MODELS:
        
        # (Trend Type, Analytic Attr)
        trend_types = [('search', search_attr), ('history', history_attr)]

        if TagModel is not None:
            filters = list(TagModel.objects.all().order_by('id'))
            analytic_attr = 'tag_id'
            trend_attr = 'tag'
            filt_model_name = TagModel.__name__
            is_tag_type = True
        elif AnalyticsModel == CalorieAnalytics:
            filters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            analytic_attr = 'calorie_level'
            trend_attr = 'calorie_level'
            filt_model_name = 'Calorie Level'
            is_tag_type = False
        else:
            print("Invalid Model Data")
            exit()

        if sim_datetime is None:
            current_datestamp = timezone.now()
        else:
            current_datestamp = sim_datetime

        analytics_set = AnalyticsModel.objects.all()
        objs_to_create = []

        print(f'{TrendsModel.__name__}:')
        for filt in filters:
            analytics = analytics_set.filter(**{analytic_attr: filt})

            filter_id = filt.id if is_tag_type else filt
            trend_data = trends.calculate(analytics, trend_types, f'{filt_model_name} - {filter_id}')

            if trend_data is None:
                continue

            for entry in trend_data:
                entry[trend_attr] = filt
                obj = TrendsModel(**entry, date_stamp=current_datestamp)

                # print(f'{obj} | Size in Bytes: {sys.getsizeof(serialize("json", [obj]))}') #DEBUG
                objs_to_create.append(obj)
        
        TrendsModel.objects.bulk_create(objs_to_create)     # @425 bytes per model, ~157.9K bulk per
        print(f"\tNumber Created: {len(objs_to_create)}\n")

   