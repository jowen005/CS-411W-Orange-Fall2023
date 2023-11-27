
# import restaurants.models as rm
# import patron.models as pm
# from ..models import RestrictionTagExclusionReport

# def driver():

#     # Grab Every Search Since Last Analytic

#     searches = pm.PatronSearchHistory.objects.all()

#     for search in searches:
#         excluded_items = rm.MenuItem.objects.exclude(menu_allergy_tag = alle)


# def exclusion_analysis():
#     pass


# excluded_items = MenuItem.objects.exclude(menu_allergy_tag = allergy)
            # for item in excluded_items:
            #     record = MenuItem.objects.get_or_create(menu_item=item, tag=allergy)
            #     record.count += 1
            #     record.save()