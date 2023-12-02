from django.utils import timezone
from datetime import datetime, timedelta
from dataclasses import dataclass
from django.core.serializers import serialize
import sys
import time

import restaurants.models as rm
import patron.models as pm
from ..models import (AllergyTagExclusionRecord, IngredientTagExclusionRecord,
                      RestrictionTagExclusionRecord, TasteTagExclusionRecord,
                      OverallExclusionRecord) #Only Stores Most Recent Info

@dataclass
class Exclusion:
    count: int = 0
    is_excluded: bool = False

def driver():

    # Since Last Analytic (Data in exclusive ranges)
    # try:
    #     latest_datestamp = OverallExclusionRecord.objects.latest('date_stamp').date_stamp
    # except OverallExclusionRecord.DoesNotExist:
    #     latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)

    # Past 3 Days (Data Overlap)
    latest_datestamp = timezone.now() - timedelta(days=3)
    
    searches = pm.PatronSearchHistory.objects.filter(search_datetime__gte=latest_datestamp)
    menu_items = rm.MenuItem.objects.all().order_by('id')
    current_datestamp = timezone.now()

    TAG_TYPES = [('allergy', rm.AllergyTag, AllergyTagExclusionRecord), 
                 ('ingredients', rm.IngredientTag, IngredientTagExclusionRecord), 
                 ('restrictions', rm.RestrictionTag, RestrictionTagExclusionRecord),
                 ('taste', rm.TasteTag, TasteTagExclusionRecord)]
    
    tag_sets = {tag_type: TagModel.objects.all().order_by('id') for tag_type, TagModel, *_ in TAG_TYPES}

    # Perform Analysis
    overall_exclusions, tag_exclusions = analysis(searches, menu_items, tag_sets, TAG_TYPES)

    # Store data
    store_overall_exclusions(overall_exclusions, menu_items, current_datestamp)
    store_tag_exclusions(tag_exclusions, menu_items, tag_sets, TAG_TYPES)


def analysis(searches, menu_items, tag_sets, TAG_TYPES):
    overall_exclusions = {f'{item.id}': Exclusion() for item in menu_items}
    tag_exclusions = {
        tag_type: {
            f'{item.id}': {
                f'{tag.id}':0 for tag in tag_sets[tag_type]}
            for item in menu_items} 
        for tag_type, *_ in TAG_TYPES
    }
    
    for search in searches:
        # Excluded if item has allergy tag
        for allergy in search.allergy_tags.all():
            excluded_items = menu_items.filter(menu_allergy_tag=allergy)
            for item in excluded_items:
                tag_exclusions['allergy'][f'{item.id}'][f'{allergy.id}'] += 1
                if not overall_exclusions[f'{item.id}'].is_excluded:
                    overall_exclusions[f'{item.id}'].count += 1

        # Excluded if item has any of the disliked ingredients (record tags that led to it getting excluded)
        for ingredient in search.disliked_ingredients.all():
            excluded_items = menu_items.filter(ingredients_tag=ingredient)
            for item in excluded_items:
                tag_exclusions['ingredients'][f'{item.id}'][f'{ingredient.id}'] += 1
                if not overall_exclusions[f'{item.id}'].is_excluded:
                    overall_exclusions[f'{item.id}'].count += 1

        # Excluded if item does not have restriction tag
        for restriction in search.dietary_restriction_tags.all():
            excluded_items = menu_items.exclude(menu_restriction_tag=restriction)
            for item in excluded_items:
                tag_exclusions['restrictions'][f'{item.id}'][f'{restriction.id}'] += 1
                if not overall_exclusions[f'{item.id}'].is_excluded:
                    overall_exclusions[f'{item.id}'].count += 1

        # Excluded if item does not have any of the taste tags (record tags that led to it getting excluded)
        excluded_items = menu_items.exclude(taste_tags__in=search.patron_taste_tags.all())
        for item in excluded_items:
            for taste in search.patron_taste_tags.all():
                tag_exclusions['taste'][f'{item.id}'][f'{taste.id}'] += 1
                if not overall_exclusions[f'{item.id}'].is_excluded:
                    overall_exclusions[f'{item.id}'].count += 1
        
        # Reset flag for next search
        for item in menu_items:
            overall_exclusions[f'{item.id}'].is_excluded = False

    return overall_exclusions, tag_exclusions


def store_overall_exclusions(overall_exclusions, menu_items, current_datestamp):
    overall_set = OverallExclusionRecord.objects.all()
    overall_to_update = []
    overall_to_create = []
    start_time = time.time()

    print(OverallExclusionRecord.__name__)
    for item in menu_items:
        try:
            record = overall_set.get(menu_item=item)
            record.exclusion_count = overall_exclusions[f'{item.id}'].count
            record.date_stamp = current_datestamp

            overall_to_update.append(record)
            # print(f'Updated: {record} | Size in Bytes: {sys.getsizeof(serialize("json", [record]))}')#NOTE

        except OverallExclusionRecord.DoesNotExist:
            record = OverallExclusionRecord(
                menu_item=item, 
                exclusion_count=overall_exclusions[f'{item.id}'].count, 
                date_stamp=current_datestamp
            )
            overall_to_create.append(record)
            # print(f'Created: {record} | Size in Bytes: {sys.getsizeof(serialize("json", [record]))}') #NOTE

    OverallExclusionRecord.objects.bulk_update(overall_to_update, fields=['exclusion_count', 'date_stamp'])
    print(f"\tNumber Updated: {len(overall_to_update)}") #NOTE
    OverallExclusionRecord.objects.bulk_create(overall_to_create)
    print(f"\tNumber Created: {len(overall_to_create)}") #NOTE

    end_time = time.time()
    print(f'\tTime to execute: {end_time - start_time} seconds')
    print('\n')


def store_tag_exclusions(tag_exclusions, menu_items, tag_sets, TAG_TYPES):
    analytic_sets = {tag_type: ExclusionModel.objects.all() for tag_type, _, ExclusionModel in TAG_TYPES}

    for tag_type, _, ExclusionModel in TAG_TYPES:
        tag_records_to_update = []
        tag_records_to_create = []
        start_time = time.time()

        print(ExclusionModel.__name__)
        for item in menu_items:    
            for tag in tag_sets[tag_type]:
                try:
                    record = analytic_sets[tag_type].get(menu_item=item, tag=tag)
                    record.exclusion_count = tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}']
                    # record.date_stamp = current_datestamp
                
                    tag_records_to_update.append(record)
                    # print(f'Updated: {record} | Size in Bytes: {sys.getsizeof(serialize("json", [record]))}')#NOTE
                    
                except ExclusionModel.DoesNotExist:
                    record = ExclusionModel(
                        menu_item=item, 
                        tag=tag, 
                        exclusion_count=tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}'], 
                        # date_stamp=current_datestamp
                    )
                    tag_records_to_create.append(record)
                    # print(f'Created: {record} | Size in Bytes: {sys.getsizeof(serialize("json", [record]))}') #NOTE
                    
        ExclusionModel.objects.bulk_update(tag_records_to_update, fields=['exclusion_count'])
        print(f"\tNumber Updated: {len(tag_records_to_update)}") #NOTE
        ExclusionModel.objects.bulk_create(tag_records_to_create)
        print(f"\tNumber Created: {len(tag_records_to_create)}") #NOTE

        end_time = time.time()
        print(f'\tTime to execute: {end_time - start_time} seconds')
        print('\n')
