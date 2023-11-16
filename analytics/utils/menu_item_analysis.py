import patron.models as pm
import restaurants.models as rm


# For total since, grab the datetime of the last analysis
    # latest_timestamp = AnalysisModel.objects.latest(timestamp) #TODO

# Then add the following filter parameter
    # datetime__gt=latest_timestamp #TODO

# Number of searches Menu Items were excluded from (total since)


def driver():
    item_ids = rm.MenuItem.objects.all().order_by('id').values_list('id', flat=True)

    num_bm_with_item = [0 for _ in range(len(item_ids))]
    num_adds_with_item = [0 for _ in range(len(item_ids))]


    for idx in range(len(item_ids)):
        num_bm_with_item[idx] = pm.Bookmark.objects.filter(
            menu_item__id=item_ids[idx] #TODO
        )
        num_adds_with_item[idx] = pm.MenuItemHistory.objects.filter(
            menu_item__id=item_ids[idx] #TODO
        )

