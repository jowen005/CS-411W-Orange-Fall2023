from restaurants.models import MenuItem
from patron.models import Patron

def quickSearch(patron_ID, query_string):
    patron = Patrons.objects.get(patron_ID)
    callorie_range = (0,patron.calorie_limit)
    if(patron.price_preference == '$'):
        price_max = 25.0
    if(patron.price_preference == '$$'):
        price_max = 50.0
    if(patron.price_preference == '$$$'):
        price_max = 1000.0
    restriction_tags = list(patron.patron_restriction_tag)
    allergy_tags = list(patron.patron_allergy_tag)
    excluded_ingredient_tags = list(patron.disliked_ingredients)
    taste_tags = list(patron.patron_taste_tag)

    return advancedSearch(query_string ,callorie_range,price_max,restriction_tags,allergy_tags,excluded_ingredient_tags,taste_tags)


#this function will hit the database twice, once to pull the patron profile and again with the actual search query.
#since all the values set by the patron profile are specified in an advanced search patron_ID is not provided
#
#returns a list of menu item IDs matching the search
def advancedSearch(query_string:str, callorie_range:tuple=(0,10000), price_range:tuple=(0.0,10000.0),
                   restriction_tags:list=None, allergy_tags:list=None, excluded_ingredient_tags:list=None,
                   taste_tags:list=None, style:list=None, time=None, sortMethod:int=0):
    #select from menuitems where restriction_tags is true and allergy_tags is false and excluded_ingredient_tags is false and taste_tags is true and style = style and resturant_hours < time 
    
    #acording to the django docs the database shouldn't be queried until the query object is evaluated so we should be able to stack filters without
    #thrashing the database with tiny queries
    
    #todo time filter
    #conceptual method:
    #get day of week from time.day
    #big ol' if block
    #Restuarants = Resturant.objects.filter(open__gte=time,close__lte=time)
    

    #todo add nullable functionality for the optional sections.  || DONE
    MenuItems = MenuItem.objects.all()
    #the most restrictive tag is likely the allergy tags so we'll filter on that first
    if allergy_tags is not None:
        MenuItems = MenuItems.exclude(menu_allergy_tag__in = allergy_tags)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
    if excluded_ingredient_tags is not None:
        MenuItems = MenuItems.exclude(ingredients_tag__in = excluded_ingredient_tags)
        #current SQL query should look like SELECT * from MenuItems
                                           #WHERE NOT (AllergyTag IN list(allergy_tags));
                                           #AND NOT(IngredientTag IN list(excluded_ingredient_tags))

        #note to self this may need to be reworked as a loop to ensure that ALL restriction tags are match
       
        #todo test the above theory.
    if restriction_tags is not None:
        MenuItems = MenuItems.filter(menu_restriction_tag__in = restriction_tags)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
                                        #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                        #AND (RestrictionTag IN list(restriction_Tags))
    if taste_tags is not None:
        MenuItems = MenuItems.filter(taste_tags__in = taste_tags)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
                                        #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                        #AND (RestrictionTag IN list(restriction_Tags))
                                        #AND (taste_tags IN list(taste_tags))
    if style is not None:
        #menu items can only have one style tag so this shouldn't need the above rework.
        MenuItems = MenuItems.filter(cook_style_tags__in = style)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
                                        #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                        #AND (RestrictionTag IN list(restriction_Tags))
                                        #AND (TasteTag IN list(taste_tags))
                                        #AND (cook_style_tags IN list(style))
    if price_range is not None:        
        MenuItems = MenuItems.filter(price__range = price_range)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
                                        #AND NOT(IngredientTag IN list(excluded_ingredient_tags))
                                        #AND (RestrictionTag IN list(restriction_Tags))
                                        #AND (TasteTag IN list(taste_tags))
                                        #AND (CookStyleTag IN list(style))
                                        #AND price BETWEEN price_range[0] and price_range[1];
    if callorie_range is not None:        
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
    if (query_string != ""):
        for queryElement in query_string.split(" "):
            #input should be clean before getting here but JUST IN CASE we'll do a little input sanitization
            queryElement = queryElement.replace('\"','')
            queryElement = queryElement.strip()

            if(queryElement[0] == '-'):
                #remove the first character ("-")
                queryElement = queryElement[1:]
                MenuItems = MenuItems.exclude(item_name__icontains = queryElement)
            else:
                MenuItems = MenuItems.filter(item_name__icontains = queryElement)
    
    #for debug purposes remove when finished
    print(MenuItems.query)

    #now we should finally be ready to evaluate the query and ping the database
    return MenuItems.values_list("id",flat=True)
    