
import patron.models as pm
import restaurants.models as rm


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


def tag_analysis(TagModel, patron_attr, menu_item_attr, search_attr, history_attr):
    tag_ids = list(TagModel.objects.all().order_by('id').values_list('id', flat=True))

    num_profiles_with_tag = [0 for _ in range(len(tag_ids))]
    num_menu_items_with_tag = [0 for _ in range(len(tag_ids))]
    num_searches_with_tag = [0 for _ in range(len(tag_ids))]
    num_adds_with_tag = [0 for _ in range(len(tag_ids))]

    for idx in range(len(tag_ids)):
        num_profiles_with_tag[idx] = pm.Patron.objects.filter(
           **{patron_attr + '__id': tag_ids[idx]}
        ).count()
        num_menu_items_with_tag[idx] = rm.MenuItem.objects.filter(
            **{menu_item_attr + '__id': tag_ids[idx]}
        ).count()
        num_searches_with_tag[idx] = pm.PatronSearchHistory.objects.filter(
            **{search_attr + '__id': tag_ids[idx]} #TODO
        ).count()
        num_adds_with_tag[idx] = pm.MenuItemHistory.objects.filter(
            **{history_attr + '__id': tag_ids[idx]} #TODO
        ).count()


def restriction_tag_analysis():
    tag_analysis(rm.RestrictionTag, 'patron_restriction_tag',
                 'menu_restriction_tag', 'dietary_restriction_tags',
                 'menu_item__menu_restriction_tag')


def allergy_tag_analysis():
    tag_analysis(rm.AllergyTag, 'patron_allergy_tag', 'menu_allergy_tag', 
                 'allergy_tags', 'menu_item__menu_allergy_tag')


def taste_tag_analysis():
    tag_analysis(rm.TasteTag, 'patron_taste_tag', 'taste_tags', 
                 'patron_taste_tags', 'menu_item__taste_tags')
    

def ingredient_tag_analysis():
    tag_analysis(rm.TasteTag, 'disliked_ingredients', 'ingredients_tag', 
                 'disliked_ingredients', 'menu_item__ingredients_tag')
    

def cook_style_tag_analysis():
    tag_titles = list(rm.CookStyleTag.objects.all().order_by('id').values_list('id', flat=True))

    num_menu_items_with_tag = [0 for _ in range(len(tag_titles))]
    num_searches_with_tag = [0 for _ in range(len(tag_titles))]
    num_adds_with_tag = [0 for _ in range(len(tag_titles))]

    for idx in range(len(tag_titles)):
        num_menu_items_with_tag[idx] = rm.MenuItem.objects.filter(
            cook_style_tags__title=tag_titles[idx]
        ).count()
        num_searches_with_tag[idx] = pm.PatronSearchHistory.objects.filter(
            query__icontains=tag_titles[idx] #TODO
        ).count()
        num_adds_with_tag[idx] = pm.MenuItemHistory.objects.filter( 
            menu_item__cook_style_tags__title=tag_titles[idx] #TODO
        ).count()


# def restriction_tag_analysis():
#     tag_ids = list(rm.RestrictionTag.objects.all().values_list('id', flat=True))

#     num_profiles_with_tag = [0 for _ in range(len(tag_ids))]
#     num_menu_items_with_tag = [0 for _ in range(len(tag_ids))]
#     num_searches_with_tag = [0 for _ in range(len(tag_ids))]
#     num_adds_with_tag = [0 for _ in range(len(tag_ids))]

#     for idx in range(len(tag_ids)):
#         num_profiles_with_tag[idx] = pm.Patron.objects.filter(
#             patron_restriction_tag__id=tag_ids[idx]
#         ).count()
#         num_menu_items_with_tag[idx] = rm.MenuItem.objects.filter(
#             menu_restriction_tag__id=tag_ids[idx]
#         ).count()
#         num_searches_with_tag[idx] = pm.PatronSearchHistory.objects.filter(
#             dietary_restriction_tags__id=tag_ids[idx]
#         ).count()
#         num_adds_with_tag[idx] = pm.MenuItemHistory.objects.filter(
#             menu_item__menu_restriction_tag__id=tag_ids[idx]
#         ).count()


# def allergy_tag_analysis():
#     tag_ids = list(rm.AllergyTag.objects.all().values_list('id', flat=True))

#     num_profiles_with_tag = [0 for _ in range(len(tag_ids))]
#     num_menu_items_with_tag = [0 for _ in range(len(tag_ids))]
#     num_searches_with_tag = [0 for _ in range(len(tag_ids))]
#     num_adds_with_tag = [0 for _ in range(len(tag_ids))]

#     for idx in range(len(tag_ids)):
#         num_profiles_with_tag[idx] = pm.Patron.objects.filter(
#             patron_allergy_tag__id=tag_ids[idx]
#         ).count()
#         num_menu_items_with_tag[idx] = rm.MenuItem.objects.filter(
#             menu_allergy_tag__id=tag_ids[idx]
#         ).count()
#         num_searches_with_tag[idx] = pm.PatronSearchHistory.objects.filter(
#             allergy_tags__id=tag_ids[idx]
#         ).count()
#         num_adds_with_tag[idx] = pm.MenuItemHistory.objects.filter(
#             menu_item__menu_allergy_tag__id=tag_ids[idx]
#         ).count()


# def taste_tag_analysis():
#     tag_ids = list(rm.TasteTag.objects.all().values_list('id', flat=True))

#     num_profiles_with_tag = [0 for _ in range(len(tag_ids))]
#     num_menu_items_with_tag = [0 for _ in range(len(tag_ids))]
#     num_searches_with_tag = [0 for _ in range(len(tag_ids))]
#     num_adds_with_tag = [0 for _ in range(len(tag_ids))]

#     for idx in range(len(tag_ids)):
#         num_profiles_with_tag[idx] = pm.Patron.objects.filter(
#             patron_taste_tag__id=tag_ids[idx]
#         ).count()
#         num_menu_items_with_tag[idx] = rm.MenuItem.objects.filter(
#             taste_tags__id=tag_ids[idx]
#         ).count()
#         num_searches_with_tag[idx] = pm.PatronSearchHistory.objects.filter(
#             patron_taste_tags__id=tag_ids[idx]
#         ).count()
#         num_adds_with_tag[idx] = pm.MenuItemHistory.objects.filter(
#             menu_item__taste_tags__id=tag_ids[idx]
#         ).count()


# def ingredient_tag_analysis():
#     tag_ids = list(rm.IngredientTag.objects.all().values_list('id', flat=True))

#     num_profiles_with_tag = [0 for _ in range(len(tag_ids))]
#     num_menu_items_with_tag = [0 for _ in range(len(tag_ids))]
#     num_searches_with_tag = [0 for _ in range(len(tag_ids))]
#     num_adds_with_tag = [0 for _ in range(len(tag_ids))]

#     for idx in range(len(tag_ids)):
#         num_profiles_with_tag[idx] = pm.Patron.objects.filter(
#             disliked_ingredients__id=tag_ids[idx]
#         ).count()
#         num_menu_items_with_tag[idx] = rm.MenuItem.objects.filter(
#             ingredients_tag__id=tag_ids[idx]
#         ).count()
#         num_searches_with_tag[idx] = pm.PatronSearchHistory.objects.filter(
#             disliked_ingredients__id=tag_ids[idx]
#         ).count()
#         num_adds_with_tag[idx] = pm.MenuItemHistory.objects.filter(
#             menu_item__ingredients_tag__id=tag_ids[idx]
#         ).count()