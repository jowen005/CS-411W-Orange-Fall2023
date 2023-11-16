
import patron.models as pm
import restaurants.models as rm


# For total since, grab the datetime of the last analysis
    # latest_timestamp = AnalysisModel.objects.latest(timestamp) #TODO

# Then add the following filter parameter
    # datetime__gt=latest_timestamp #TODO


def driver():
    
    lower_bounds = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                    1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
    upper_bounds = [99, 199, 299, 399, 499, 599, 699, 799, 899, 999, 1099,
                    1199, 1299, 1399, 1499, 1599, 1699, 1799, 1899, 1999, -1]
    
    num_profiles_in_range = [0 for _ in range(len(lower_bounds))]
    num_menu_items_in_range = [0 for _ in range(len(lower_bounds))]
    num_searches_in_range = [0 for _ in range(len(lower_bounds))]
    num_adds_in_range = [0 for _ in range(len(lower_bounds))]

    for idx in range(len(lower_bounds)):
        if upper_bounds[idx] == -1:
            num_profiles_in_range[idx] = pm.Patron.objects.filter(
                calorie_limit__gte=lower_bounds[idx]
            ).count()

            num_menu_items_in_range[idx] = rm.MenuItem.objects.filter(
                calories__gte=lower_bounds[idx]
            ).count()

            num_searches_in_range[idx] = pm.PatronSearchHistory.objects.filter(
                calorie_limit__gte=lower_bounds[idx] #TODO
            ).count()

            num_adds_in_range[idx] = pm.MenuItemHistory.objects.filter(
                menu_item__calories__gte=lower_bounds[idx] #TODO
            ).count()

        # Number of profiles within range (total)
        num_profiles_in_range[idx] = pm.Patron.objects.filter(
            calorie_limit__gte=lower_bounds[idx],
            calorie_limit__lte=upper_bounds[idx]
        ).count()

        # Number of menu items within range (total)
        num_menu_items_in_range[idx] = rm.MenuItem.objects.filter(
            calories__gte=lower_bounds[idx],
            calories__lte=upper_bounds[idx]
        ).count()

        # Number of searches within range (total since) #TODO
        num_searches_in_range[idx] = pm.PatronSearchHistory.objects.filter(
            calorie_limit__gte=lower_bounds[idx],
            calorie_limit__lte=upper_bounds[idx]
        ).count()

        # Number of items added to history within range (total since) #TODO
        num_adds_in_range[idx] = pm.MenuItemHistory.objects.filter(
            menu_item__calories__gte=lower_bounds[idx],
            menu_item__calories__lte=upper_bounds[idx]
        ).count()

    print(f'Profile Calorie Analysis:') #NOTE
    for idx in range(len(lower_bounds)-1):  #NOTE
        print(f'\t{lower_bounds[idx]}-{upper_bounds[idx]}: {num_profiles_in_range[idx]}')  #NOTE
    print(f'\t{lower_bounds[-1]} and up: {num_profiles_in_range[-1]}\n') #NOTE

    print(f'Menu Item Calorie Analysis:') #NOTE
    for idx in range(len(lower_bounds)-1):  #NOTE
        print(f'\t{lower_bounds[idx]}-{upper_bounds[idx]}: {num_menu_items_in_range[idx]}')  #NOTE
    print(f'\t{lower_bounds[-1]} and up: {num_menu_items_in_range[-1]}\n') #NOTE

    print(f'Search Calorie Analysis:') #NOTE
    for idx in range(len(lower_bounds)-1):  #NOTE
        print(f'\t{lower_bounds[idx]}-{upper_bounds[idx]}: {num_searches_in_range[idx]}')  #NOTE
    print(f'\t{lower_bounds[-1]} and up: {num_searches_in_range[-1]}\n') #NOTE

    print(f'Menu Item History Calorie Analysis:') #NOTE
    for idx in range(len(lower_bounds)-1):  #NOTE
        print(f'\t{lower_bounds[idx]}-{upper_bounds[idx]}: {num_adds_in_range[idx]}')  #NOTE
    print(f'\t{lower_bounds[-1]} and up: {num_adds_in_range[-1]}\n') #NOTE
