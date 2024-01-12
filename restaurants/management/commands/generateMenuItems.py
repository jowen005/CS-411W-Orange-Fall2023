from pathlib import Path
import random
import json
from lcc_project.commands.generate import GenerateCommand, add_file_path
from restaurants.models import TasteTag,CookStyleTag,FoodTypeTag,AllergyTag,RestrictionTag,Restaurant,IngredientTag

@add_file_path
class Command(GenerateCommand):
    DEFAULT_JSON_PATH = 'json_files/menuItemsBuffer.json'
    TAG_RELATIONS_PATH = "json_files/tagRelations.json"
    def generate(self, count:int):

        monarch_user = self.User.objects.get(email="monarch@odu.edu")
        monarch_rest_ids = Restaurant.objects.filter(owner=monarch_user).values_list("id",flat=True)

        valid_ingredient_tag = [
            "anchovy_paste", "banana", "basil", "beans", "beef", "beef_broth", "bell_pepper", "black_pepper",
            "butter", "butterfly", "butternut_squash", "cane_sugar", "canola_oil", "carrot", "cheese", "chicken",
            "chicken_broth", "chickpeas", "chili_powder", "cinnamon", "chocolate", "corn", "corn_oil", "corn_starch",
            "cream", "cricket", "duck", "eggs", "fish", "garlic", "gluten", "high_fructose_corn_syrup", "honey",
            "horseradish", "lemon", "lentils", "lettuce", "milk", "mushroom", "mustard", "nuts", "olive_oil", "onion",
            "oregano", "parmesan", "peanuts", "pickle", "pork", "potato", "potato_starch", "red_pepper", "rice",
            "salt", "sesame", "shellfish", "sherry", "soy", "spinach", "strawberry", "tomato", "turkey", "vanilla",
            "veal", "venison", "vinegar", "wheat"
        ]

        valid_owners = list(Restaurant.objects.all().values_list('id',flat=True))
        for monarch_id in monarch_rest_ids:
            valid_owners.remove(monarch_id)
        valid_food_type_tag = list(FoodTypeTag.objects.values_list('id',flat=True))
        valid_cook_style_tags = list(CookStyleTag.objects.values_list('id',flat=True))
        valid_taste_tags = list(TasteTag.objects.values_list('id',flat=True))


        data_list = []
        for _ in range(count):
            #Generate and Store Data
            # Randomly choose 2-5 ingredients
            num_ingredients = random.randint(2, min(5, len(valid_ingredient_tag)))
            chosen_ingredients = random.sample(valid_ingredient_tag,num_ingredients)

            ingredients_tags = set()
            ingredient_indices = {title: IngredientTag.objects.get(title=title).id for title in valid_ingredient_tag}
            for ingredient in chosen_ingredients:
                if ingredient in valid_ingredient_tag:
                    ingredients_tags.add(ingredient_indices[ingredient])
                    
            menuItem_type = [" Bowl", " Tacos", " Noodle", " Pizza", " Warp", " Roll", " Over Rice", " Burger", " Curry" , " Fritter", " Stir-fry", " Teriyaki"]
            # Update the menuitem_name with 1 elements from chosen_ingredients
            menuitem_names = random.sample(chosen_ingredients, 1) + random.sample(menuItem_type, 1)

            # Map chosen ingredients to their respective allergy tags
            allergy_values = list(AllergyTag.objects.values_list('title', flat=True).order_by('id'))
            allergy_ids = list(AllergyTag.objects.values_list('id', flat=True).order_by('id'))
            allergy_indices = {value: allergy_ids[index] for index, value in enumerate(allergy_values)}
            # print(allergy_indices)
            #print("Allergen values:", allergy_indices)
            APP_DIR = Path(__file__).resolve().parent.parent
            try:
                with open(APP_DIR/self.TAG_RELATIONS_PATH) as infile:
                    tagRelations = json.load(infile)
            except IOError:
                    self.stdout.write(self.style.ERROR(f"Input of tag relation file failed!"))
                    exit()
            allergy_tags = set()
                #check if any allergy
            for allergen_ingredient in chosen_ingredients:
                for allergy_type, allergens in tagRelations['allergies'].items():
                    if allergen_ingredient in allergens:
                        allergy_tags.add(allergy_indices[allergy_type])
            
            # Get the restriction values for each ingredient
            restriction_tags = set()

            # # Create a mapping of restriction values to their respective indices (+1)
            def_restriction_values = list(RestrictionTag.objects.values_list('title', flat=True).order_by('id'))
            def_restriction_ids = list(RestrictionTag.objects.values_list('id', flat=True).order_by('id'))
            restriction_indices = {value: def_restriction_ids[index] for index, value in enumerate(def_restriction_values)}
            
            valid_restrictions = def_restriction_values
            for res_ing in chosen_ingredients:
                for tag, conflicts in tagRelations['restrictions'].items():
                    if res_ing in conflicts and tag in valid_restrictions:
                        valid_restrictions.remove(tag)

            for res_ing in valid_restrictions:
                restriction_tags.add(restriction_indices[res_ing])

            data = {
                "restaurant_id": random.choice(valid_owners),
                "item_name": ' '.join(menuitem_names),
                "price": round(random.uniform(7.50, 25.55),2),
                "calories": random.randint(250, 1800),

                "food_type_tag_id": random.choice(valid_food_type_tag),
                "taste_tags": list(set(self.fake.random_choices(elements=valid_taste_tags))),
                "cook_style_tags_id": random.choice(valid_cook_style_tags),

                "menu_restriction_id": list(restriction_tags),
                "ingredients_tag": list(ingredients_tags),
                "menu_allergy_tag": list(allergy_tags),
                
                "time_of_day_available": 'Anytime',
                "is_modifiable": False
            }

            data_list.append(data)

        return data_list
    
