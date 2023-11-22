from datetime import datetime
from django.utils import timezone

import patron.models as pm
import restaurants.models as rm
from ..models import (RestrictionTagAnalytics, AllergiesTagAnalytics, 
                      TasteTagAnalytics, IngredientTagAnalytics, CookStyleAnalytics)

# For total since, grab the datetime of the last analysis
    # latest_timestamp = AnalysisModel.objects.latest(timestamp) #TODO

# Then add the following filter parameter
    # datetime__gt=latest_timestamp #TODO

def driver():
    restriction_tag_analysis()
    allergy_tag_analysis()
    taste_tag_analysis()
    ingredient_tag_analysis()
    cook_style_tag_analysis()


def get_latest_datetime(AnalyticsModel):
    try:
        latest_datestamp = AnalyticsModel.objects.latest('date_stamp').date_stamp
    except AnalyticsModel.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    return latest_datestamp


def store_data(AnalyticsModel, tag_data):
    for entry in tag_data:
        print(entry) #NOTE
        # obj = AnalyticsModel.objects.create(**entry)
        # print(f'{obj}')
    print('\n') #NOTE


def restriction_tag_analysis():
    tag_analysis(rm.RestrictionTag, RestrictionTagAnalytics, 
                 patron_attr='patron_restriction_tag',
                 menu_item_attr='menu_restriction_tag', 
                 search_attr='dietary_restriction_tags',
                 history_attr='menu_item__menu_restriction_tag')


def allergy_tag_analysis():
    tag_analysis(rm.AllergyTag, AllergiesTagAnalytics, 
                 patron_attr='patron_allergy_tag', 
                 menu_item_attr='menu_allergy_tag', 
                 search_attr='allergy_tags', 
                 history_attr='menu_item__menu_allergy_tag')


def taste_tag_analysis():
    tag_analysis(rm.TasteTag, TasteTagAnalytics, 
                 patron_attr='patron_taste_tag', 
                 menu_item_attr='taste_tags', 
                 search_attr='patron_taste_tags', 
                 history_attr='menu_item__taste_tags')
    

def ingredient_tag_analysis():
    tag_analysis(rm.IngredientTag, IngredientTagAnalytics, 
                 patron_attr='disliked_ingredients', 
                 menu_item_attr='ingredients_tag', 
                 search_attr='disliked_ingredients', 
                 history_attr='menu_item__ingredients_tag')


def cook_style_tag_analysis():
    tag_analysis(rm.CookStyleTag, CookStyleAnalytics) #attributes defined explicitly
    


def tag_analysis(TagModel, AnalyticsModel, patron_attr='', menu_item_attr='', search_attr='', history_attr=''):
    tags = list(TagModel.objects.all().order_by('id'))
    tag_data = []

    latest_datestamp = get_latest_datetime(AnalyticsModel)
    
    if TagModel == rm.CookStyleTag:
        for tag in tags:
            data = {}

            data['tag_id'] = tag
            data['number_of_menuItem'] = rm.MenuItem.objects.filter(
                cook_style_tags__id=tag.id
            ).count()
            data['number_of_search'] = pm.PatronSearchHistory.objects.filter(
                query__icontains=tag.title,
                search_datetime__gt=latest_datestamp
            ).count()
            data['number_of_HIS'] = pm.MenuItemHistory.objects.filter( 
                menu_item__cook_style_tags__id=tag.id,
                MenuItemHS_datetime__gt=latest_datestamp
            ).count()

            tag_data.append(data)
    else:
        for tag in tags:
            data = {}

            data['tag_id'] = tag
            data['number_of_patronProfile'] = pm.Patron.objects.filter(
            **{patron_attr + '__id': tag.id}
            ).count()
            data['number_of_menuItem'] = rm.MenuItem.objects.filter(
                **{menu_item_attr + '__id': tag.id}
            ).count()
            data['number_of_search'] = pm.PatronSearchHistory.objects.filter(
                **{search_attr + '__id': tag.id},
                search_datetime__gt=latest_datestamp
            ).count()
            data['number_of_HIS'] = pm.MenuItemHistory.objects.filter(
                **{history_attr + '__id': tag.id},
                MenuItemHS_datetime__gt=latest_datestamp
            ).count()

            tag_data.append(data)
        
    store_data(AnalyticsModel, tag_data)
    