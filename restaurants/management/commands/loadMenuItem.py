from restaurants.models import MenuItem, RestTag, FoodTypeTag, CookStyleTag, AllergyTag, RestrictionTag,TasteTag,IngredientTag
from lcc_project.commands.load import LoadCommand, add_file_path


@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/menuItems.json'


    def load(self, data_list):
        for obj in data_list:
            restaurant_id = obj.pop('restaurant')
            food_type_tag_id = obj.pop('food_type_tag')
            taste_tags_id = obj.pop('tase_tags')
            cook_style_tags_id = obj.pop('cook_style_tags')
            menu_allergy_tag_id = obj.pop('menu_allergy_tag')
            menu_restriction_tag_id = obj.pop('menu_restriction_tag')
            ingredients_tag_id = obj.pop('ingredients_tag')
            #Retrieve objects references by PKFields
            restaurant = self.User.objects.get(pk=restaurant_id)   # Format for ForeignKey/OneToOneFields
            food_type_tag = [FoodTypeTag.objects.get(pk=tag_id) for tag_id in food_type_tag_id]   #Format for ManyToManyFields
            taste_tags = [TasteTag.objects.get(pk=tag_id) for tag_id in taste_tags_id]
            cook_style_tags = [CookStyleTag.objects.get(pk=tag_id) for tag_id in cook_style_tags_id]
            menu_restriction_tag = [RestrictionTag.objects.get(pk=tag_id) for tag_id in menu_restriction_tag_id]
            menu_allergy_tag = [AllergyTag.objects.get(pk=tag_id) for tag_id in menu_allergy_tag_id]
            ingredients_tag = [IngredientTag.objects.get(pk=tag_id) for tag_id in ingredients_tag_id]
            #Create object
            item = MenuItem.objects.create(restaurant=restaurant, **obj)
            item.taste_tags.set(taste_tags)
            item.cook_style_tags.set(cook_style_tags)
            item.food_type_tag.set(food_type_tag)
            item.ingredients_tag.set(ingredients_tag)
            item.menu_allergy_tag.set(menu_allergy_tag)
            item.menu_restriction_tag.set(menu_restriction_tag)