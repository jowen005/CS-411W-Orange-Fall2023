from restaurants.models import MenuItem
from restaurants.models import Patron

def quickSearch(patron_ID, query_string):
    pass

#this function will hit the database twice, once to pull the patron profile and again with the actual search query.
#since all the values set by the patron profile are specified in an advanced search patron_ID is not provided
#query_string: string, callorie_range: tuple(int, int), price_range: tuple(double, double),
#restriction_tags: list, allergy_tags: list, excluded_ingredient_tags: list, taste_tags: list, style: list, time: time
#sortMethod: int
#
#returns a list of menu item IDs matching the search
def advancedSearch(query_string, callorie_range, price_range,
                   restriction_tags, allergy_tags, excluded_ingredient_tags,
                   taste_tags, style, time, sortMethod):
    #select from menuitems where restriction_tags is true and allergy_tags is false and excluded_ingredient_tags is false and taste_tags is true and style = style and resturant_hours < time 
    
    #acording to the django docs the database shouldn't be queried until the query object is evaluated so we should be able to stack filters without
    #thrashing the database with tiny queries
    
    
    #todo add nullable functionality for the optional sections.

    #the most restrictive tag is likely the allergy tags so we'll filter on that first
    MenuItems = MenuItem.objects.exclude(menu_allergy_tag__in = allergy_tags)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags));
    MenuItems = MenuItems.exclude(ingredients_tag__in = excluded_ingredient_tags)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags));
                                       #AND NOT(IngredientTag IN list(excluded_ingredient_tags))

    #note to self this may need to be reworked as a loop to ensure that ALL restriction tags are match
    #todo test the above theory.
    MenuItems = MenuItems.filter(menu_restriction_tag__in = restriction_tags)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags));
                                       #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                       #AND (RestrictionTag IN list(restriction_Tags))
    MenuItems = MenuItems.filter(taste_tags__in = taste_tags)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags));
                                       #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                       #AND (RestrictionTag IN list(restriction_Tags))
                                       #AND (taste_tags IN list(taste_tags))

    #menu items can only have one style tag so this shouldn't need the above rework.
    MenuItems = MenuItems.filter(cook_style_tags__in = style)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags));
                                       #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                       #AND (RestrictionTag IN list(restriction_Tags))
                                       #AND (TasteTag IN list(taste_tags))
                                       #AND (cook_style_tags IN list(style))
    MenuItems = MenuItems.filter(price__range = price_range)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags));
                                       #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                       #AND (RestrictionTag IN list(restriction_Tags))
                                       #AND (TasteTag IN list(taste_tags))
                                       #AND (CookStyleTag IN list(style))
                                       #AND price BETWEEN price_range[0] and price_range[1];
    MenuItems = MenuItems.filter(calories__range = callorie_range)
    #current SQL query should look like SELECT * from MenuItems
                                       #WHERE NOT (AllergyTag IN list(allergy_tags))
                                       #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                       #AND (RestrictionTag IN list(restriction_Tags))
                                       #AND (TasteTag IN list(taste_tags))
                                       #AND (CookStyleTag IN list(style))
                                       #AND price BETWEEN price_range[0] and price_range[1]
                                       #AND calories BETWEEN callorie_range[0] and callorie_range[1]

    #now it gets complicated and hard to track what the query should look like                                
    #theoretically we can save the query string until last weirdly
    for queryElement in split(query_string, " ")
        if ('\"' in queryElement):
            #first lets clean those qoutes of 
            queryElement = queryElement.replace('\"','')
        queryElement = queryElement.strip()
        if(queryElement[0] = '-'):
            queryElement = queryElement[1:]
            MenuItems = MenuItems.objects.exclude(name__contains = queryElement)
        else:
            MenuItems = MenuItems.objects.filter(name__contains = queryElement)
    
    #now we should finally be ready to evaluate the query and ping the database
    return MenuItems.values_list("id",flat=true)
    