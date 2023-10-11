from faker import Faker
import random

from lcc_project.commands.generate import GenerateCommand, add_file_path
from restaurants.models import TasteTag,CookStyleTag,FoodTypeTag,AllergyTag,RestrictionTag

@add_file_path
class Command(GenerateCommand):
    DEFAULT_JSON_PATH = 'json_files/menuItems.json'

    def generate(self, count:int):

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
            "butterfly": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"], 
            "butternut_squash": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cane_sugar": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "canola_oil": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "carrot": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cheese": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "milk"],
            "chicken": ["halal", "kosher"],
            "chicken_broth": ["halal", "kosher"],
            "chickpeas": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "chili_powder": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "cinnamon": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "chocolate": ["vegetarian", "halal", "kosher", "keto", "pescetarian", "dairy-free","milk"],
            "corn": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "corn_oil": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
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
            "pork": ["halal", "kosher"],
            "potato": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "potato_starch": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "red_pepper": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "rice": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "salt": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo"],
            "sesame": ["vegetarian", "vegan", "halal", "kosher", "keto", "pescetarian", "dairy-free", "paleo", "sesame"],
            "shellfish": ["halal", "kosher", "shellfish"],
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

        valid_owners = list(self.User.objects.filter(user_type='restaurant').values_list('id',flat=True))
        valid_food_type_tag = list(FoodTypeTag.objects.values_list('id',flat=True))
        valid_cook_style_tags = list(CookStyleTag.objects.values_list('id',flat=True))
        valid_taste_tags = list(TasteTag.objects.values_list('id',flat=True))

        
        data_list = []
        for _ in range(count):
            #Generate and Store Data
            # Randomly choose 2-5 ingredients
            num_ingredients = random.randint(2, min(5, len(valid_ingredient_tag)))
            chosen_ingredients = random.sample(valid_ingredient_tag,num_ingredients)
            # Update the menuitem_name with 2 elements from chosen_ingredients
            menuitem_names = random.sample(chosen_ingredients, 2)

            # Map chosen ingredients to their respective allergy tags
            allergy_values = set(AllergyTag.objects.values_list('title', flat=True))
            #print("Allergen values:", allergy_values)
            allergy_tags = set()
                #check if any allergy
            for ingredient in chosen_ingredients:
                if ingredient in ingredient_to_allergy_mapping:
                    for allergy_value in ingredient_to_allergy_mapping[ingredient]:
                        if allergy_value in allergy_values:
                           allergy_tags.add(allergy_value)

            
            # Get the restriction values associated with RestrictionTag
            restriction_values = list(RestrictionTag.objects.values_list('title', flat=True))
            # Get the restriction values for each ingredient
            ingredient_restriction_values = []
            restriction_tags = set()

            for ingredient in chosen_ingredients:
                if ingredient in ingredient_to_allergy_mapping:
                    # Gather all the restriction values for each ingredient
                    restriction_values = ingredient_to_allergy_mapping[ingredient]
                    ingredient_restriction_values.append(set(restriction_values))

            # Check if all ingredients have the same restriction value
            if all(restriction_set == ingredient_restriction_values[0] for restriction_set in ingredient_restriction_values):
                common_restriction_value = ingredient_restriction_values[0]
                restriction_tags.update(common_restriction_value)



            data = {
                "restaurant": random.choice(valid_owners),
                "name": menuitem_names,
                "price": round(random.uniform(7.50, 25.55),2),
                "calories": random.randint(250, 1800),

                "food_type_tag": random.choice(valid_food_type_tag),
                "taste_tags": random.choice(valid_taste_tags),
                "cook_style_tags": random.choice(valid_cook_style_tags),

                "menu_restriction_tag": list(restriction_tags),
                "ingredients_tag": chosen_ingredients,
                "menu_allergy_tag": list(allergy_tags),
                
                "time_of_day_available": 'Anytime',
                "is_modifiable": False
            }

            data_list.append(data)

        return data_list