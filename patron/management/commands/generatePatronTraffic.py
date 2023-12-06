from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from faker import Faker

import json
from pathlib import Path
import random
import math
from patron.utils.search import advancedSearch

import restaurants.models as rm
import patron.models as pm
import patron.serializers as ps
from feedback.models import Reviews

SEARCH_TYPES = ['quick', 'advanced']
SEARCH_WEIGHTS = [5, 2]

BOOKMARK_SELECTIONS = [0, 1, 2, 3]
BOOKMARK_WEIGHTS = [1, 2, 3, 2]

HISTORY_SELECTIONS = [0, 1]
HISTORY_WEIGHTS = [2, 1]

RATING_VALUES = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
RATING_WEIGHTS =   [1,   2,   3,   4,   5,   6,   5,   4,   3,   2,   1]

class Command(BaseCommand):

    help = 'Generate and insert fake patron interaction data'
    TAG_RELATIONS_PATH = "json_files/tagRelations.json"
    DEFAULT_JSON_PATH = "json_files/test.json"
    User = get_user_model()
    fake = Faker()

    possible_reviews = [
        'This menu item was terrible',  # rating 0 & 0.5
        'This menu item was not good',  # rating 1 & 1.5
        'This menu item was alright',   # rating 2 & 2.5
        '',                             # rating 3 & 3.5
        'This menu item good',          # rating 4 & 4.5
        'This menu item was excellent'  # rating 5
    ]


    def add_arguments(self, parser: CommandParser):
        parser.add_argument("userid", nargs=1, type=int)
        parser.add_argument('-n', dest='num_searches', default=1, type=int, 
                            help='Specifies a number of searches')


    def handle(self, userid, num_searches, *args, **kwargs):
        APP_DIR = Path(__file__).resolve().parent.parent

        # Tag Relation File
        try:
            with open(APP_DIR/self.TAG_RELATIONS_PATH) as infile:
                tag_relations = json.load(infile)
        except IOError:
            self.stdout.write(self.style.ERROR(f"Input of tag relation file failed!"))
            exit()

        user, profile = self.verify_user(userid[0])



        search_report = self.generate_search_traffic(user, profile, tag_relations, num_searches)
        bookmark_report = self.generate_bookmark_traffic(user)
        self.output_reports(search_report, bookmark_report)

        self.stdout.write(self.style.SUCCESS(f"{num_searches} search(es) were performed!"))


    def verify_user(self, userid: int):
        try:
            user = self.User.objects.get(id=userid)
        except self.User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'A user with ID {userid} does not exist!'))
            exit()

        if user.user_type != 'patron':
            self.stdout.write(self.style.ERROR(f'The user ({user.email}) with ID {userid} is not a patron!'))
            exit()

        try:
            profile = pm.Patron.objects.get(user=user)
            return user, profile
        except pm.Patron.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'This user ({user.email}) does not have an associated profile!'))
            exit()
        

    def generate_search_traffic(self, user: User, profile: pm.Patron, tag_relations ,num_searches:int =1):
        
        ingredients = list(rm.IngredientTag.objects.values_list('title',flat=True))
        # decisions = ['quick', 'advanced']
        search_report = [{} for _ in range(num_searches)]

        for idx in range(num_searches):
            decision = random.choices(SEARCH_TYPES, weights=SEARCH_WEIGHTS, k=1)[0]
            # decision = decisions[1] #Force Advanced Search

            print('='*100) #NOTE
            print(f'Search {idx}: {decision}') #NOTE
            print('='*100) #NOTE
            
            # Generate and Add Search to Search History
            if decision == 'quick':
                search_inst = self.generate_quick_search(user, profile, tag_relations, ingredients)
            else:
                search_inst = self.generate_advanced_search(user, tag_relations, ingredients)

            search_obj = self.format_search_object(search_inst)

            print(f'Search Object submitted to search:\n\t{search_obj}\n') #NOTE

            # Perform Search
            result_ids = list(advancedSearch(**search_obj))

            # Initialize Search Report
            search_report[idx] = {
                'results': len(result_ids),
                'bookmark': 0,
                'itemhistory': 0,
            }

            print(f'Result IDs: {result_ids}\n') #NOTE

            # Bookmark Menu Items
            bookmarks = self.generate_bookmarks(user, result_ids)
            if bookmarks is not None:
                search_report[idx]['bookmark'] = len(bookmarks)
            else:
                self.stdout.write(self.style.ERROR(f"No results found on Search {idx}."))
                continue

            print(f'Remaining Results: {result_ids}\n') #NOTE

            # Add Items to Menu Item History
            items_added = self.generate_item_history(user, result_ids)
            if items_added is not None:
                search_report[idx]['itemhistory'] = len(items_added)
            else:
                self.stdout.write(self.style.ERROR(f"All results have been bookmarked on Search {idx}."))
                continue

            print(f'Items Added: {items_added}') #NOTE

        return search_report
    

    def generate_quick_search(self, user: User, profile: pm.Patron, tag_relations, valid_queries):
        # Remove possible queries that conflict with tag selections
        for ingred in list(profile.disliked_ingredients.all()):
            if ingred.title in valid_queries:
                valid_queries.remove(ingred.title)
                
        for restr in list(profile.patron_restriction_tag.all()): 
            for conflict in tag_relations['restrictions'][f'{restr.title}']:
                if conflict in valid_queries:
                    valid_queries.remove(conflict)

        for allergy in list(profile.patron_allergy_tag.all()):
            for conflict in tag_relations['allergies'][f'{allergy.title}']:
                if conflict in valid_queries:
                    valid_queries.remove(conflict)

        # Add Quick Search object to Search History
        search_data = {
            "patron": user,
            "query": random.choice(valid_queries),
            "calorie_limit": profile.calorie_limit,
            "price_min": 0.02,
            "price_max": profile.price_max
        }

        print(f'Search Data: {search_data}') #NOTE
        
        search_inst = pm.PatronSearchHistory.objects.create(**search_data)
        search_inst.dietary_restriction_tags.set(profile.patron_restriction_tag.all())
        search_inst.allergy_tags.set(profile.patron_allergy_tag.all())
        search_inst.patron_taste_tags.set(profile.patron_taste_tag.all())
        search_inst.disliked_ingredients.set(profile.disliked_ingredients.all())

        print(f'Search Tags for {search_inst}\n\tRestrc: {list(search_inst.dietary_restriction_tags.all())}\n\t'+ #NOTE
              f'Allerg: {list(search_inst.allergy_tags.all())}\n\tTaste:  {list(search_inst.patron_taste_tags.all())}\n\t'+ #NOTE
              f'DisIng: {list(search_inst.disliked_ingredients.all())}') #NOTE

        return search_inst
    

    def generate_advanced_search(self, user: User, tag_relations, valid_queries):
        # Grab Valid Tags
        valid_restrict_tags = list(rm.RestrictionTag.objects.all())
        valid_allergy_tags = list(rm.AllergyTag.objects.all())
        valid_taste_tags = list(rm.TasteTag.objects.all())
        valid_ingred_tags = list(rm.IngredientTag.objects.all())

        # Make Selections
        num_selections = [0, 1, 2]
        selected_restrict_tags = random.sample(valid_restrict_tags, 
                                    k=random.choices(num_selections, weights=[3,2,1], k=1)[0])
        selected_allergy_tags = random.sample(valid_allergy_tags, 
                                    k=random.choices(num_selections, weights=[3,2,1], k=1)[0])
        selected_taste_tags = random.sample(valid_taste_tags, 
                                    k=random.choices(num_selections, weights=[3,2,1], k=1)[0])
        selected_ingred_tags = random.sample(valid_ingred_tags, 
                                    k=random.choices(num_selections, weights=[3,2,1], k=1)[0])
        
        # print(f'Tag Selections: \n\t{selected_restrict_tags}\n\t{selected_allergy_tags}\n\t{selected_taste_tags}\n\t{selected_ingred_tags}\n')
        # print(f'Valid Queries: {valid_queries}')
        
        # Remove possible queries that conflict with tag selections
        for ingred in selected_ingred_tags:
            if ingred.title in valid_queries:
                valid_queries.remove(ingred.title)
                
        for restr in selected_restrict_tags: 
            for conflict in tag_relations['restrictions'][f'{restr.title}']:
                if conflict in valid_queries:
                    valid_queries.remove(conflict)

        for allergy in selected_allergy_tags:
            for conflict in tag_relations['allergies'][f'{allergy.title}']:
                if conflict in valid_queries:
                    valid_queries.remove(conflict)

        print(f'Valid Queries: {valid_queries}')

        # Add Advanced Search object to Search History
        search_data = {
            "patron": user,
            "query": random.choice(valid_queries),
            "calorie_limit": random.randint(250, 2200),
            "price_min": 0.02,
            "price_max": 30.0 # NOTE: Adjust to be random
        }

        print(f'Search Data: {search_data}') #NOTE
        
        search_inst = pm.PatronSearchHistory.objects.create(**search_data)
        search_inst.dietary_restriction_tags.set(selected_restrict_tags)
        search_inst.allergy_tags.set(selected_allergy_tags)
        search_inst.patron_taste_tags.set(selected_taste_tags)
        search_inst.disliked_ingredients.set(selected_ingred_tags)

        print(f'Search Tags for {search_inst}\n\tRestrc: {list(search_inst.dietary_restriction_tags.all())}\n\t'+ #NOTE
              f'Allerg: {list(search_inst.allergy_tags.all())}\n\tTaste:  {list(search_inst.patron_taste_tags.all())}\n\t'+ #NOTE
              f'DisIng: {list(search_inst.disliked_ingredients.all())}') #NOTE

        return search_inst
    

    def format_search_object(self, search_inst):
        search_serializer = ps.PatronSearchHistorySerializer(instance=search_inst)
        search_obj = search_serializer.data
        search_obj['search_datetime'] = search_inst.search_datetime
        search_obj.pop('id')
        search_obj.pop('patron')
        search_obj.pop('calorie_level')

        return search_obj
    

    def generate_bookmarks(self, user: User, result_ids):
        # num_nonbookmark_results = len(result_ids)
        # find menu items that have not been bookmarked
        bookmark_item_ids = list(pm.Bookmark.objects.filter(patron=user).values_list('menu_item', flat=True))
        nonbookmarked_results = [item for item in result_ids if item not in bookmark_item_ids]
        num_nonbookmark_results = len(nonbookmarked_results)
        
        print(f'Bookmark Item IDs: {bookmark_item_ids}') #NOTE
        print(f'NonBookmarked Results: {nonbookmarked_results}') #NOTE
        print(f'Number of nonbookmarked results: {num_nonbookmark_results}\n') #NOTE

        if num_nonbookmark_results == 0:
            return None

        choice = random.choices(BOOKMARK_SELECTIONS, weights=BOOKMARK_WEIGHTS, k=1)[0]
        num_bookmarks = min(choice, num_nonbookmark_results)
        print(f'Number of bookmarks to be selected: {num_bookmarks}') #NOTE
        
        bookmarks = []

        # Create Bookmarks
        if num_bookmarks != 0:
            # grab random bookmarkable items
            for item_id in random.sample(nonbookmarked_results, k=num_bookmarks):
                result_ids.remove(item_id)

                item = rm.MenuItem.objects.get(id=item_id)
                bookmarks.append(pm.Bookmark.objects.create(patron=user, menu_item=item))
                print(f'Menu Item Bookmarked: {item_id}') #NOTE

        print(f'Successful Bookmarks: {bookmarks}\n') #NOTE

        return bookmarks


    def generate_item_history(self, user: User, result_ids):
        num_results = len(result_ids)

        if num_results == 0:
            return None

        choice = random.choices(HISTORY_SELECTIONS, weights=HISTORY_WEIGHTS, k=1)[0]
        num_adds = min(num_results, choice)
        print(f'Number of items to be added: {num_adds}') #NOTE

        items_added = []

        if num_adds != 0:
            for item_id in random.sample(result_ids, k=num_adds): # num_adds == 1 (loop for robustness)
                result_ids.remove(item_id)

                item = rm.MenuItem.objects.get(id=item_id)
                
                # Generate and Create Feedback object
                rating = random.choices(RATING_VALUES, weights=RATING_WEIGHTS, k=1)[0]
                feedback_data = {
                    "patron": user,
                    "menu_item": item,
                    "rating": rating,
                    "review": self.possible_reviews[math.floor(rating)]
                }

                print(f'Feedback Data: {feedback_data}') #NOTE
                feedback_obj = Reviews.objects.create(**feedback_data)
                print(f'Feedback Object Successful: {feedback_obj}') #NOTE

                # Create Menu Item History Object
                items_added.append(pm.MenuItemHistory.objects.create(patron=user, review=feedback_obj, menu_item=item))
                print(f'Menu Item Added: {item_id}') #NOTE

            print(f'Successful Adds: {items_added}\n') #NOTE

        return items_added


    def generate_bookmark_traffic(self, user: User):

        print('='*100) #NOTE
        print(f'Bookmark Traffic') #NOTE
        print('='*100+'\n') #NOTE

        valid_bookmarks = list(pm.Bookmark.objects.all())
        items_added = []

        num_bookmarks = len(valid_bookmarks)

        print(f'Number of Bookmarks {num_bookmarks}') #NOTE

        if num_bookmarks == 0:
            return {'itemsadded':0, 'itemsremaining':0}
        elif num_bookmarks == 1:
            num_selections = 1
        elif num_bookmarks <= 5:
            num_selections = num_bookmarks - 1
        else:
            num_selections = num_bookmarks - 3

        print(f'Number of Selections: {num_selections}') #NOTE

        for bookmark in random.sample(valid_bookmarks, k=num_selections):
            item = bookmark.menu_item
            bookmark.delete()

            rating = random.choices(RATING_VALUES, weights=RATING_WEIGHTS, k=1)[0]
            feedback_data = {
                "patron": user,
                "menu_item": item,
                "rating": rating,
                "review": self.possible_reviews[math.floor(rating)]
            }

            print(f'Feedback Data: {feedback_data}') #NOTE

            feedback_obj = Reviews.objects.create(**feedback_data)

            items_added.append(pm.MenuItemHistory.objects.create(patron=user, review=feedback_obj, menu_item=item))

            print(f'Menu Item Added: {item}') #NOTE

        bookmark_report = {}
        bookmark_report['itemsadded'] = len(items_added)
        bookmark_report['itemsremaining'] = num_bookmarks - num_selections

        print('\n') #NOTE

        return bookmark_report
    

    def output_reports(self, search_report, bookmark_report):

        num_searches = len(search_report)

        print("-"*50)
        print("generatePatronTraffic Report")
        print("-"*50)

        print('\n|' + '-'*63 +'|')
        print('| Search # | # of Results | # of Bookmarks | # Added to History |')
        print('|----------|--------------|----------------|--------------------|')
        
        for idx in range(num_searches):
            print(f'|    {idx+1:>5} |     {search_report[idx]["results"]:>8} ' +
                  f'|       {search_report[idx]["bookmark"]:>8} ' +
                  f'|           {search_report[idx]["itemhistory"]:>8} |')
            
        print('|' + '-'*63 +'|\n')

        print(f'{bookmark_report["itemsadded"]} Menu Items were removed from the Bookmark List and Added to the Menu Item History.')
        print(f'{bookmark_report["itemsremaining"]} Menu Items still remain in the Bookmark List\n')
    