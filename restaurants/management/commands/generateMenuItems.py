from faker import Faker
import random

from lcc_project.commands.generate import GenerateCommand, add_file_path
from restaurants.models import TasteTag,CookStyleTag,FoodTypeTag,AllergyTag,RestrictionTag,Restaurant,IngredientTag

@add_file_path
class Command(GenerateCommand):
    DEFAULT_JSON_PATH = 'json_files/menuItemsBuffer.json'

    def generate(self, count:int):

        monarch_user = self.User.objects.get(email="monarch@odu.edu")
        monarch_rest_ids = Restaurant.objects.filter(owner=monarch_user).values_list("id",flat=True)

        ingredient_to_allergy_mapping = {
            "anchovy_paste": ["halal", "kosher","fish"],
            "banana": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "basil": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "beans": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo", "soybeans"],
            "beef": ["halal", "kosher"],
            "beef_broth": ["halal", "kosher"],
            "bell-pepper": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "black_pepper": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "butter": ["vegetarian", "halal", "kosher", "keto", "pescetarian"],
            "butterfly": ["vegetarian", "vegan", "keto", "pescetarian", "dairy-free", "paleo"], 
            "butternut_squash": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cane_sugar": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "canola_oil": ["vegetarian", "vegan", "keto", "pescetarian", "dairy-free", "paleo"],
            "carrot": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cheese": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "milk"],
            "chicken": ["halal", "kosher"],
            "chicken_broth": ["halal", "kosher"],
            "chickpeas": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "chili_powder": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cinnamon": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "chocolate": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "dairy-free","milk"],
            "corn": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "corn_oil": ["vegetarian", "vegan", "keto", "pescetarian", "dairy-free", "paleo"],
            "corn_starch": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cream": ["vegetarian", "halal", "kosher", "keto", "pescetarian","milk"],
            "cricket": ["halal", "kosher"],
            "duck": ["halal", "kosher"],
            "eggs": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "eggs"],
            "fish": ["halal", "kosher", "fish"],
            "garlic": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "gluten": ["halal", "kosher", "celiac"],
            "high_fructose_corn_syrup": ["halal", "kosher"],
            "honey": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "horseradish": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "lemon": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "lentils": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "lettuce": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "milk": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "milk"],
            "mushroom": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "mustard": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "nuts": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "tree_nuts"],
            "olive_oil": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "onion": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "oregano": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "parmesan": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "milk"],
            "peanuts": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "tree_nuts"],
            "pickle": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "pork": [],
            "potato": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "potato_starch": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "red_pepper": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "rice": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "salt": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "sesame": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo", "sesame"],
            "shellfish": ["shellfish"],
            "sherry": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "soy": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "soybeans"],
            "spinach": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "strawberry": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "tomato": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "turkey": ["halal", "kosher"],
            "vanilla": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "veal": ["halal", "kosher"],
            "venison": ["halal", "kosher"],
            "vinegar": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "wheat": ["halal", "kosher", "wheat"]
        }

        valid_ingredient_tag = [
            "anchovy_paste", "banana", "basil", "beans", "beef", "beef_broth", "bell-pepper", "black_pepper",
            "butter", "butterfly", "butternut_squash", "cane_sugar", "canola_oil", "carrot", "cheese", "chicken",
            "chicken_broth", "chickpeas", "chili_powder", "cinnamon", "chocolate", "corn", "corn_oil", "corn_starch",
            "cream", "cricket", "duck", "eggs", "fish", "garlic", "gluten", "high_fructose_corn_syrup", "honey",
            "horseradish", "lemon", "lentils", "lettuce", "milk", "mushroom", "mustard", "nuts", "olive_oil", "onion",
            "oregano", "parmesan", "peanuts", "pickle", "pork", "potato", "potato_starch", "red_pepper", "rice",
            "salt", "sesame", "shellfish", "sherry", "soy", "spinach", "strawberry", "tomato", "turkey", "vanilla",
            "veal", "venison", "vinegar", "wheat"
        ]

        # valid_owners = list(self.User.objects.filter(user_type='restaurant').values_list('id',flat=True))
        valid_owners = list(Restaurant.objects.all().values_list('id',flat=True))
        for monarch_id in monarch_rest_ids:
            valid_owners.remove(monarch_id)
        valid_food_type_tag = list(FoodTypeTag.objects.values_list('id',flat=True))
        valid_cook_style_tags = list(CookStyleTag.objects.values_list('id',flat=True))
        valid_taste_tags = list(TasteTag.objects.values_list('id',flat=True))

        # for tag in AllergyTag.objects.all():
        #     print(f'{tag.id} - {tag.title}')

        # print('\n')
        # for tag in RestrictionTag.objects.all():
        #     print(f'{tag.id} - {tag.title}')

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

            # Update the menuitem_name with 2 elements from chosen_ingredients
            menuitem_names = random.sample(chosen_ingredients, 2)

            # Map chosen ingredients to their respective allergy tags
            allergy_values = list(AllergyTag.objects.values_list('title', flat=True).order_by('id'))
            allergy_ids = list(AllergyTag.objects.values_list('id', flat=True).order_by('id'))
            #print("Allergen values:", allergy_values)
            # a dictionary of allergy_title, allergy_id pairs
            # allergy_indices = {allergy_value: index + 1 for index, allergy_value in enumerate(allergy_values)}

            allergy_indices = {value: allergy_ids[index] for index, value in enumerate(allergy_values)}
            # print(allergy_indices)
            
            #print("Allergen values:", allergy_indices)
            allergy_tags = set()
                #check if any allergy
            for allergen_ingredient in chosen_ingredients:
                if allergen_ingredient in ingredient_to_allergy_mapping:
                    for allergy_value in ingredient_to_allergy_mapping[allergen_ingredient]:
                        if allergy_value in allergy_values:
                           allergy_tags.add(allergy_indices[allergy_value])
            
      # Get the restriction values associated with RestrictionTag
            restriction_values = list(RestrictionTag.objects.values_list('title', flat=True).order_by('id'))
            # Get the restriction values for each ingredient
            restriction_tags = set()
            # Initialize a set to store common restriction values
            common_restriction_values = None

            for ingredient in chosen_ingredients:
                if ingredient in ingredient_to_allergy_mapping:
                    # Gather all the restriction values for each ingredient
                    restriction_values = set(ingredient_to_allergy_mapping[ingredient])
                    
                    # Update common restriction values on the first iteration
                    if common_restriction_values is None:
                        common_restriction_values = restriction_values
                    else:
                        # Update common restriction values by taking the intersection
                        common_restriction_values.intersection_update(restriction_values)
            
            # Check if all ingredients have the common restriction values
            if common_restriction_values is not None:
                restriction_tags.update(common_restriction_values)
            # Create a mapping of restriction values to their respective indices (+1)
            def_restriction_values = list(RestrictionTag.objects.values_list('title', flat=True).order_by('id'))
            def_restriction_ids = list(RestrictionTag.objects.values_list('id', flat=True).order_by('id'))
            restriction_indices = {value: def_restriction_ids[index] for index, value in enumerate(def_restriction_values)}
            # print(f'{restriction_indices}\n')
            
            #print("Updated restriction_tags_id:", restriction_indices)
            # Initialize a mapping to store the index (+1) of each common restriction value
            restriction_tags_id = set()
            for restriction in common_restriction_values:
                    if restriction in def_restriction_values:
                        restriction_tags_id.add(restriction_indices[restriction])

            data = {
                "restaurant_id": random.choice(valid_owners),
                "item_name": ' '.join(menuitem_names),
                "price": round(random.uniform(7.50, 25.55),2),
                "calories": random.randint(250, 1800),

                "food_type_tag_id": random.choice(valid_food_type_tag),
                "taste_tags": list(set(self.fake.random_choices(elements=valid_taste_tags))),
                "cook_style_tags_id": random.choice(valid_cook_style_tags),

                "menu_restriction_id": list(restriction_tags_id),
                "ingredients_tag": list(ingredients_tags),
                "menu_allergy_tag": list(allergy_tags),
                
                "time_of_day_available": 'Anytime',
                "is_modifiable": False
            }

            data_list.append(data)

        return data_list