from django.utils import timezone
from datetime import datetime
from dataclasses import dataclass

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

    try:
        latest_datestamp = OverallExclusionRecord.objects.latest('date_stamp').date_stamp
    except OverallExclusionRecord.DoesNotExist:
        latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    
    searches = pm.PatronSearchHistory.filter(search_datetime__gte=latest_datestamp)
    menu_items = rm.MenuItem.objects.all().order_by('id')
    current_datestamp = timezone.now()

    tag_item_collection(searches, menu_items, current_datestamp)


def tag_item_collection(searches, menu_items, current_datestamp, TAG_TYPES):
    TAG_TYPES = [('allergy', rm.AllergyTag, AllergyTagExclusionRecord), 
                 ('ingredients', rm.IngredientTag, IngredientTagExclusionRecord), 
                 ('restrictions', rm.RestrictionTag, RestrictionTagExclusionRecord),
                 ('taste', rm.TasteTag, TasteTagExclusionRecord)]
    
    tag_sets = {tag_type: TagModel.objects.all() for tag_type, TagModel, *_ in TAG_TYPES}

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

    analytic_sets = {tag_type: ExclusionModel.objects.all() for tag_type, _, ExclusionModel in TAG_TYPES}
    overall_set = OverallExclusionRecord.objects.all()

    # For bulk update
    # tag_records_to_update = []
    # tag_records_to_create = []
    # overall_to_update = []
    # overall_to_create = []

    # Overall Exclusions
    print('Overall Exclusions')
    for item in menu_items:
        try:

            print(f'{item.id} --> {overall_exclusions[f"{item.id}"].count}') #NOTE
            # record = overall_set.get(menu_item=item)
            # record.exclusion_count = overall_exclusions[f'{item.id}'].count
            # record.date_stamp = current_datestamp
            # record.save()
            # print(f'Updated: {record}')
            # overall_to_update.append(record)

        except ExclusionModel.DoesNotExist:
            record = ExclusionModel.objects.create(
                menu_item=item, 
                exclusion_count=overall_exclusions[f'{item.id}'].count, 
                date_stamp=current_datestamp
            )
            print(f'Created: {record}')
            # overall_to_create.append(ExclusionModel(
            #     menu_item=item, 
            #     exclusion_count=overall_exclusions[f'{item.id}'].count, 
            #     date_stamp=current_datestamp
            # ))
    print('\n')

    # Tag Exclusions
    for tag_type, _, ExclusionModel in TAG_TYPES:
        print(f'Tag Type: {tag_type}') #NOTE
        for item in menu_items:    
            for tag in tag_sets[tag_type]:
                try:
                    print(f"{item.id}: {tag.id} --> {tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}']}") #NOTE
                    # tag_record = analytic_sets[tag_type].get(menu_item=item, tag=tag)
                    # tag_record.exclusion_count = tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}']
                    # tag_record.date_stamp = current_datestamp
                    # tag_record.save()
                    # print(f'Updated: {record}')
                    # tag_records_to_update.append(record)

                except ExclusionModel.DoesNotExist:
                    record = ExclusionModel.objects.create(
                        menu_item=item, 
                        tag=tag, 
                        exclusion_count=tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}'], 
                        date_stamp=current_datestamp
                    )
                    print(f'Created: {record}')
                    # tag_records_to_create.append(ExclusionModel(
                    #     menu_item=item, 
                    #     tag=tag, 
                    #     exclusion_count=tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}'], 
                    #     date_stamp=current_datestamp
                    # ))
        print('\n')
        
    #     ExclusionModel.objects.bulk_update(tag_records_to_update)
    #     ExclusionModel.objects.bulk_create(tag_records_to_create)

    # OverallExclusionRecord.objects.bulk_update(overall_to_update)
    # OverallExclusionRecord.objects.bulk_create(overall_to_create)




# DEADDDDD

#     for tag_type, _, ExclusionModel in TAG_TYPES:
#         for item in menu_items:
#             # Update Overall Exclusions
#             try:
#                 record = overall_set.get(menu_item=item)
#                 record.exclusion_count += overall_exclusions[f'{item.id}'].count
#                 record.date_stamp = current_datestamp
#                 record.save()
#                 # overall_to_update.append(record)

#             except ExclusionModel.DoesNotExist:
#                 ExclusionModel.objects.create(
#                     menu_item=item, 
#                     exclusion_count=overall_exclusions[f'{item.id}'].count, 
#                     date_stamp=current_datestamp
#                 )
#                 # overall_to_create.append(ExclusionModel(
#                 #     menu_item=item, 
#                 #     exclusion_count=overall_exclusions[f'{item.id}'].count, 
#                 #     date_stamp=current_datestamp
#                 # ))
            
#             for tag in tag_sets[tag_type]:
#                 # Update Tag Exclusions
#                 try:
#                     tag_record = analytic_sets[tag_type].get(menu_item=item, tag=tag)
#                     tag_record.exclusion_count += tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}']
#                     tag_record.date_stamp = current_datestamp
#                     tag_record.save()
#                     # tag_records_to_update.append(record)

#                 except ExclusionModel.DoesNotExist:
#                     ExclusionModel.objects.create(
#                         menu_item=item, 
#                         tag=tag, 
#                         exclusion_count=tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}'], 
#                         date_stamp=current_datestamp
#                     )
#                     # tag_records_to_create.append(ExclusionModel(
#                     #     menu_item=item, 
#                     #     tag=tag, 
#                     #     exclusion_count=tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}'], 
#                     #     date_stamp=current_datestamp
#                     # ))
        
#     #     ExclusionModel.objects.bulk_update(tag_records_to_update)
#     #     ExclusionModel.objects.bulk_create(tag_records_to_create)

#     # OverallExclusionRecord.objects.bulk_update(overall_to_update)
#     # OverallExclusionRecord.objects.bulk_create(overall_to_create)










    