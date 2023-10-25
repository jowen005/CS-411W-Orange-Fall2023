from restaurants.models import Restaurant, MenuItem, FoodTypeTag, CookStyleTag, AllergyTag, RestrictionTag, TasteTag, IngredientTag
from lcc_project.commands.load import LoadCommand, add_file_path

@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/menuItemsBuffer.json'

    def load(self, data_list):
        for obj in data_list:
            restaurant_id = obj.pop('restaurant_id')
            food_type_tag_id = obj.pop('food_type_tag_id')
            taste_tags_id = obj.pop('taste_tags')
            cook_style_tags_id = obj.pop('cook_style_tags_id')
            menu_allergy_tag_id = obj.pop('menu_allergy_tag')
            menu_restriction_id = obj.pop('menu_restriction_id')
            ingredients_tag_id = obj.pop('ingredients_tag')

            # Retrieve objects references by PKFields
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            food_type_tag = FoodTypeTag.objects.get(pk=food_type_tag_id)
            # taste_tags = TasteTag.objects.get(pk=taste_tags_id)
            cook_style_tags = CookStyleTag.objects.get(pk=cook_style_tags_id)

            menu_restriction_tag = [RestrictionTag.objects.get(pk=id) for id in menu_restriction_id]
            menu_allergy_tag = [AllergyTag.objects.get(pk=id) for id in menu_allergy_tag_id]
            ingredients_tag = [IngredientTag.objects.get(pk=id) for id in ingredients_tag_id]
            taste_tags = [TasteTag.objects.get(pk=id) for id in taste_tags_id]

            # Create object
            # item = MenuItem.objects.create(
            #     restaurant=restaurant,
            #     food_type_tag=food_type_tag,
            #     cook_style_tags = cook_style_tags,
            #     item_name=obj.get('item_name'),
            #     price=obj.get('price'),
            #     calories=obj.get('calories'),
            #     time_of_day_available=obj.get('time_of_day_available'),
            #     is_modifiable=obj.get('is_modifiable'),
            # )

            item = MenuItem.objects.create(
                restaurant=restaurant,
                food_type_tag=food_type_tag,
                cook_style_tags = cook_style_tags,
                **obj
            )

            # Use a list with a single element for set() calls
            item.taste_tags.set(taste_tags)
            item.ingredients_tag.set(ingredients_tag)
            item.menu_allergy_tag.set(menu_allergy_tag)
            item.menu_restriction_tag.set(menu_restriction_tag)
 