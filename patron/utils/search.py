from restaurants.models import MenuItem
from restaurants.models import FoodTypeTag,CookStyleTag,Restaurant
from patron.models import Patron

#this function will hit the database twice, once to pull the patron profile and again with the actual search query.
#since all the values set by the patron profile are specified in an advanced search patron_ID is not provided
#
#returns a list of menu item IDs matching the search
#name kept as advanced search for compatibility reasons
def advancedSearch(query:str, calorie_limit:int=10000, price_min:float=0.0, price_max:float=100000.0,
                   dietary_restriction_tags:list=None, allergy_tags:list=None, disliked_ingredients:list=None,
                   patron_taste_tags:list=None, search_datetime=None, time_of_day_available=None):
    
    #todo add nullable functionality for the optional sections.  || DONE
    MenuItems = MenuItem.objects.all()

    #return MenuItems.values_list("id",flat=True)
    #the most restrictive tag is likely the allergy tags so we'll filter on that first
    if allergy_tags is not None:
        MenuItems = MenuItems.exclude(menu_allergy_tag__in = allergy_tags)
    if disliked_ingredients is not None:
        MenuItems = MenuItems.exclude(ingredients_tag__in = disliked_ingredients)

    #note to self this may need to be reworked as a loop to ensure that ALL restriction tags are match
    #todo test the above theory.
    print("=========================================================")
    print(str(dietary_restriction_tags))
    print( (dietary_restriction_tags is not None) and (len(dietary_restriction_tags) > 0))
    if (dietary_restriction_tags is not None) and (len(dietary_restriction_tags) > 0):
        MenuItems = MenuItems.filter(menu_restriction_tag__in = dietary_restriction_tags)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
                                        #AND NOT(IngredientTag IN list(disliked_ingredients))
                                        #AND (RestrictionTag IN list(dietary_restriction_tags))
    if (patron_taste_tags is not None) and (len(patron_taste_tags) > 0):
        MenuItems = MenuItems.filter(taste_tags__in = patron_taste_tags)
        #current SQL query should look like SELECT * from MenuItems
                                        #WHERE NOT (AllergyTag IN list(allergy_tags));
                                        #AND NOT(IngredientTag IN list(disliked_ingredients))
                                        #AND (RestrictionTag IN list(dietary_restriction_tags))
                                        #AND (patron_taste_tags IN list(patron_taste_tags))

    if price_min is not None and price_max is not None:        
        MenuItems = MenuItems.filter(price__range = (price_min,price_max))

    if calorie_limit is not None:        
        MenuItems = MenuItems.filter(calories__lte = calorie_limit)
                                       
    #theoretically we can save the query string until last weirdly
    #nice to have --> synonym dictonary for fuzzy logic on the search query.
    #todo: convert title to ID tag
    cook_style_tags = list(CookStyleTag.objects.values_list('title',flat=True))
    food_type_tags = list(FoodTypeTag.objects.values_list('title',flat=True))
    if (query != ""):
        query = query.lower()
        for queryElement in query.split(" "):
            #input should be clean before getting here but JUST IN CASE we'll do a little input sanitization
            queryElement = queryElement.replace('\"','')
            queryElement = queryElement.strip()

            if(queryElement[0] == '-'):
                #remove the first character ("-")
                queryElement = queryElement[1:]
                if(queryElement in cook_style_tags):
                    MenuItems = MenuItems.exclude(cook_style_tags = queryElement)
                elif(queryElement in food_type_tags):
                    MenuItems = MenuItems.exclude(food_type_tag = queryElement)
                else:
                    MenuItems = MenuItems.exclude(item_name__icontains = queryElement)
            else:
                if(queryElement in cook_style_tags):
                    MenuItems = MenuItems.filter(cook_style_tags = queryElement)
                elif(queryElement in food_type_tags):
                    MenuItems = MenuItems.filter(food_type_tag = queryElement)
                else:
                    MenuItems = MenuItems.filter(item_name__icontains = queryElement)   

    if(time_of_day_available != None):
        MenuItems = MenuItems.filter(time_of_day_available__in = [time, 'Anytime'])

    #datetime_object = datetime.strptime(search_datetime, '%Y-%m-%d %H:%M:%S')
    weekday = search_datetime.weekday()
    
    #might be better ways to do this, more research is needed
    #get all restuarants of menu items we've already searched
    Restaurants = Restaurant.objects.filter(id__in = MenuItems.values_list("restaurant",flat=True))
    targetTime = search_datetime#.time #.strftime("%H:%M:%S")

    print(Restaurants.values_list("id",flat=True))
     #todo: convert this to checking unix time stamp instead
    if(weekday == 0): #monday
        print("monday")
        Restaurants = Restaurants.filter(mon_open__hour__lte = targetTime.hour)
        #Restaurants = Restaurants.filter(mon_open__minute__lte = targetTime.minute)
        Restaurants = Restaurants.filter(mon_close__hour__gte = targetTime.hour)
    elif(weekday == 1): #tuesday
        print("tuesday")
        Restaurants = Restaurants.filter(tue_open__hour__lte = targetTime.hour)
        Restaurants = Restaurants.filter(tue_close__hour__gte = targetTime.hour)
    elif(weekday == 2): #wednesday
        print("wednesday")
        Restaurants = Restaurants.filter(wed_open__hour__lte = targetTime.hour)
        Restaurants = Restaurants.filter(wed_close__hour__gte = targetTime.hour)
    elif(weekday == 3): #thursday
        print("thursday")
        Restaurants = Restaurants.filter(thu_open__hour__lte = targetTime.hour)
        Restaurants = Restaurants.filter(thu_close__hour__gte = targetTime.hour)
    elif(weekday == 4): #friday
        print("friday")
        Restaurants = Restaurants.filter(fri_open__hour__lte = targetTime.hour)
        Restaurants = Restaurants.filter(fri_close__hour__gte = targetTime.hour)
    elif(weekday == 5): #saturday
        print("saturday")
        print(Restaurants.values_list("id",flat=True))
        #print(((Restaurants.values_list("sat_open",flat=True))[0]).hour)
        Restaurants = Restaurants.filter(sat_open__hour__lte = targetTime.hour)
        Restaurants = Restaurants.filter(sat_close__hour__gte = targetTime.hour)
    elif(weekday == 6): #sunday
        print("sunday")
        Restaurants = Restaurants.filter(sun_open__hour__lte = targetTime.hour)
        Restaurants = Restaurants.filter(sun_close__hour__gte = targetTime.hour)
    
    print(Restaurants.values_list("id",flat=True))
    
    #return MenuItems.values_list("id",flat=True) 
    MenuItems = MenuItems.filter(restaurant__in = Restaurants.values_list("id",flat=True))

    #for debug purposes remove when finished
    #print(MenuItems.query)
    #now we should finally be ready to evaluate the query and ping the database
    return MenuItems.values_list("id",flat=True)
    
### DEPRECIATED

# def quickSearch(patron_ID, query):
#     patron = Patrons.objects.get(patron_ID)
#     calorie_limit = (0,patron.calorie_limit)
#     if(patron.price_preference == '$'):
#         price_max = 25.0
#     if(patron.price_preference == '$$'):
#         price_max = 50.0
#     if(patron.price_preference == '$$$'):
#         price_max = 1000.0
#     dietary_restriction_tags = list(patron.patron_restriction_tag)
#     allergy_tags = list(patron.patron_allergy_tag)
#     disliked_ingredients = list(patron.disliked_ingredients)
#     patron_taste_tags = list(patron.patron_taste_tag)

#     return advancedSearch(query ,calorie_limit,price_max,dietary_restriction_tags,allergy_tags,disliked_ingredients,patron_taste_tags)

