from django.utils import timezone
from datetime import datetime
from dataclasses import dataclass

import restaurants.models as rm
import patron.models as pm

@dataclass
class Exclusion:
    count: int = 0
    is_excluded: bool = False

def driver(item_data, menu_items, searches):

    # try:
    #     latest_datestamp = OverallExclusionRecord.objects.latest('date_stamp').date_stamp
    # except OverallExclusionRecord.DoesNotExist:
    #     latest_datestamp = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    
    # searches = pm.PatronSearchHistory.filter(search_datetime__gte=latest_datestamp)
    # menu_items = rm.MenuItem.objects.all().order_by('id')
    # current_datestamp = timezone.now()
    
    TAG_TYPES = [('allergy', rm.AllergyTag), 
                 ('ingredients', rm.IngredientTag), 
                 ('restrictions', rm.RestrictionTag),
                 ('taste', rm.TasteTag)]
    
    tag_sets = {tag_type: TagModel.objects.all() for tag_type, TagModel in TAG_TYPES}

    tag_exclusions = {
        tag_type: {
            f'{item.id}': {
                f'{tag.id}':0 for tag in tag_sets[tag_type]}
            for item in menu_items} 
        for tag_type, *_ in TAG_TYPES
    }
    
    overall_exclusions = {f'{item.id}': Exclusion() for item in menu_items}

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


    # Store exclusion
    for entry in item_data:
        menu_item = entry['menuItem_id']

        #Overall Exclusion
        entry['exclusion_count'] = overall_exclusions[f'{menu_item.id}'].count

        for tag_type, *_ in TAG_TYPES:
            tag_counts = tag_exclusions[tag_type][f'{menu_item.id}']
            sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
            top_3 = sorted_tags[:3]
            
            idx, tag_dict = 1, {}
            for tag_id, count in top_3:
                tag_dict[f'{idx}'] = {
                    'title':tag_sets[tag_type].get(id=tag_id).title,
                    'count':count
                }
            entry[f'top_3_{tag_type}'] = tag_dict

    return item_data
                

        
            
            
    # analytic_sets = {tag_type: AnalyticsModel.objects.all() for tag_type, _, AnalyticsModel in TAG_TYPES}
    # overall_set = OverallExclusionRecord.objects.all()

    # # Store exclusion
    # for tag_type, _, AnalyticsModel in TAG_TYPES:
    #     for item in menu_items:
    #         try:
    #             record = overall_set.get(menu_item=item)
    #             record.exclusion_count += overall_exclusions[f'{item.id}'].count
    #             record.date_stamp = current_datestamp
    #             record.save()

    #         except AnalyticsModel.DoesNotExist:
    #             AnalyticsModel.objects.create(
    #                 menu_item=item, 
    #                 exclusion_count=overall_exclusions[f'{item.id}'].count, 
    #                 date_stamp=current_datestamp
    #             )
            
    #         for tag in tag_sets[tag_type]:
    #             try:
    #                 tag_record = analytic_sets[tag_type].get(menu_item=item, tag=tag)
    #                 tag_record.exclusion_count += tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}']
    #                 tag_record.date_stamp = current_datestamp
    #                 tag_record.save()

    #             except AnalyticsModel.DoesNotExist:
    #                 AnalyticsModel.objects.create(
    #                     menu_item=item, 
    #                     tag=tag, 
    #                     exclusion_count=tag_exclusions[tag_type][f'{item.id}'][f'{tag.id}'], 
    #                     date_stamp=current_datestamp
    #                 )

