from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max, Sum

import patron.models as pm
import restaurants.models as rm
from ..models import (RestrictionTagAnalytics, AllergiesTagAnalytics, 
                      TasteTagAnalytics, IngredientTagAnalytics, CookStyleAnalytics)

from ..models import (AllergyTagExclusionRecord, IngredientTagExclusionRecord,
                      RestrictionTagExclusionRecord, TasteTagExclusionRecord)



def driver(restriction=False, allergy=False, taste=False, ingredient=False, cook_style=False):
    
    no_analysis_specified = not (restriction or allergy or taste or ingredient or cook_style)
    if no_analysis_specified:   #Run All
        restriction_tag_analysis()
        allergy_tag_analysis()
        taste_tag_analysis()
        ingredient_tag_analysis()
        cook_style_tag_analysis()
        return
    
    if restriction:
        restriction_tag_analysis()
    if allergy:
        allergy_tag_analysis()
    if taste:
        taste_tag_analysis()
    if ingredient:
        ingredient_tag_analysis()
    if cook_style:
        cook_style_tag_analysis()


def get_latest_datetime(AnalyticsModel):
    try:
        latest_datestamp = AnalyticsModel.objects.latest('date_stamp').date_stamp
    except AnalyticsModel.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    # latest_datestamp = timezone.now() - timedelta(days=5)
    return latest_datestamp


def store_data(AnalyticsModel, tag_data, current_datestamp):
    for entry in tag_data:
        # print(entry) #NOTE
        obj = AnalyticsModel.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)
    print('\n')


def tag_analysis(TagModel, AnalyticsModel, ExclusionModel=None, 
                 patron_attr='', menu_item_attr='', search_attr='', history_attr=''):
    
    tags = list(TagModel.objects.all().order_by('id'))
    tag_data = []

    latest_datestamp = get_latest_datetime(AnalyticsModel)

    patron_set = pm.Patron.objects.all()
    item_set = rm.MenuItem.objects.all()
    search_set = pm.PatronSearchHistory.objects.filter(search_datetime__gt=latest_datestamp)
    history_set = pm.MenuItemHistory.objects.filter(MenuItemHS_datetime__gt=latest_datestamp)
    current_datestamp = timezone.now()

    if TagModel == rm.CookStyleTag:
        for tag in tags:
            data = {}

            data['tag_id'] = tag
            data['number_of_menuItem'] = item_set.filter(
                cook_style_tags__id=tag.id
            ).count()
            data['number_of_search'] = search_set.filter(
                query__icontains=tag.title
            ).count()
            data['number_of_HIS'] = history_set.filter( 
                menu_item__cook_style_tags__id=tag.id
            ).count()

            tag_data.append(data)
    else:
        exclusion_set = ExclusionModel.objects.all()

        for tag in tags:
            data = {}

            data['tag_id'] = tag
            data['number_of_patronProfile'] = patron_set.filter(
                **{patron_attr + '__id': tag.id}
            ).count()
            data['number_of_menuItem'] = item_set.filter(
                **{menu_item_attr + '__id': tag.id}
            ).count()
            data['number_of_search'] = search_set.filter(
                **{search_attr + '__id': tag.id},
            ).count()
            data['number_of_HIS'] = history_set.filter(
                **{history_attr + '__id': tag.id},
            ).count()

            result_dict = exclusion_set.filter(tag=tag).aggregate(Sum('exclusion_count'))
            data['exclusion_count'] = result_dict['exclusion_count__sum']

            tag_data.append(data)
        
    store_data(AnalyticsModel, tag_data, current_datestamp)


def restriction_tag_analysis():
    tag_analysis(rm.RestrictionTag, RestrictionTagAnalytics, RestrictionTagExclusionRecord,
                 patron_attr='patron_restriction_tag',
                 menu_item_attr='menu_restriction_tag', 
                 search_attr='dietary_restriction_tags',
                 history_attr='menu_item__menu_restriction_tag')


def allergy_tag_analysis():
    tag_analysis(rm.AllergyTag, AllergiesTagAnalytics, AllergyTagExclusionRecord,
                 patron_attr='patron_allergy_tag', 
                 menu_item_attr='menu_allergy_tag', 
                 search_attr='allergy_tags', 
                 history_attr='menu_item__menu_allergy_tag')


def taste_tag_analysis():
    tag_analysis(rm.TasteTag, TasteTagAnalytics, TasteTagExclusionRecord,
                 patron_attr='patron_taste_tag', 
                 menu_item_attr='taste_tags', 
                 search_attr='patron_taste_tags', 
                 history_attr='menu_item__taste_tags')
    

def ingredient_tag_analysis():
    tag_analysis(rm.IngredientTag, IngredientTagAnalytics, IngredientTagExclusionRecord,
                 patron_attr='disliked_ingredients', 
                 menu_item_attr='ingredients_tag', 
                 search_attr='disliked_ingredients', 
                 history_attr='menu_item__ingredients_tag')


def cook_style_tag_analysis():
    tag_analysis(rm.CookStyleTag, CookStyleAnalytics) #attributes defined explicitly
    
