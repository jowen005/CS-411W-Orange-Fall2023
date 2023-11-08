from restaurants.models import Restaurant, MenuItem, FoodTypeTag, CookStyleTag, AllergyTag, RestrictionTag, TasteTag, IngredientTag
from lcc_project.commands.load import LoadCommand, add_file_path

@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/menuitemSetup.json'
    
    def loadTagList(self, tagValue, modelTags):
        # Read the Tags values and ids from DB
        values = list(modelTags.objects.values_list('title', flat=True).order_by('id'))
        ids = list(modelTags.objects.values_list('id', flat=True).order_by('id'))
        indices = {value: ids[index] for index, value in enumerate(values)}
        tag_id = set()
        # Check and load the ids
        for value in tagValue:
            if value in values:
                tag_id.add(indices[value])
        return tag_id
    
    def loadTagStr(self, tagValue, modelTags):
        # Read the Tags values and ids from DB
        values = list(modelTags.objects.values_list('title', flat=True).order_by('id'))
        ids = list(modelTags.objects.values_list('id', flat=True).order_by('id'))
        indices = {value: ids[index] for index, value in enumerate(values)}
        tag_id = indices.get(tagValue, None)
        return tag_id
    
    def process_menu_item(self, obj, restaurant_name, updated_menuItems, created_menuItems):
        item_name = obj.pop('item_name')
        rest_names = list(Restaurant.objects.values_list('name', flat=True).order_by('id'))
        rest_ids = list(Restaurant.objects.values_list('id', flat=True).order_by('id'))
        indices = {value: rest_ids[index] for index, value in enumerate(rest_names)}
        restaurant_name = indices.get(restaurant_name, None)
        
        restaurant = Restaurant.objects.get(pk=restaurant_name)
        foodType = obj.pop('food_type_tag_id')
        food_type_tag_id = self.loadTagStr(foodType, FoodTypeTag)
        taste = obj.pop('taste_tags')
        taste_tags_id = self.loadTagList(taste, TasteTag)
        cookStyle = obj.pop('cook_style_tags_id')
        cook_style_tags_id = self.loadTagStr(cookStyle, CookStyleTag)
        allergy = obj.pop('menu_allergy_tag')
        menu_allergy_tag_id = self.loadTagList(allergy, AllergyTag)
        restriction = obj.pop('menu_restriction_id')
        menu_restriction_id = self.loadTagList(restriction, RestrictionTag)
        ingredients = obj.pop('ingredients_tag')
        ingredients_tag_id = self.loadTagList(ingredients, IngredientTag)

        # Retrieve objects referenced by primary keys
        food_type_tag = FoodTypeTag.objects.get(pk=food_type_tag_id)
        cook_style_tags = CookStyleTag.objects.get(pk=cook_style_tags_id)

        menu_restriction_tag = [RestrictionTag.objects.get(pk=id) for id in menu_restriction_id]
        menu_allergy_tag = [AllergyTag.objects.get(pk=id) for id in menu_allergy_tag_id]
        ingredients_tag = [IngredientTag.objects.get(pk=id) for id in ingredients_tag_id]
        taste_tags = [TasteTag.objects.get(pk=id) for id in taste_tags_id]
        
        # Check if menu item exists
        try:
            item = MenuItem.objects.get(item_name=item_name, restaurant=restaurant)
            updated_menuItems.append(item_name + " -> " + str(restaurant_name))
            for attr, value in obj.items():
                setattr(item, attr, value)
        except MenuItem.DoesNotExist:
            created_menuItems.append(item_name + " -> " + str(restaurant_name))
            item = MenuItem.objects.create(
                restaurant=restaurant,
                food_type_tag=food_type_tag,
                cook_style_tags=cook_style_tags,
                item_name=item_name,
                **obj
            )
        # Set the many-to-many relationships
        item.taste_tags.set(taste_tags)
        item.ingredients_tag.set(ingredients_tag)
        item.menu_allergy_tag.set(menu_allergy_tag)
        item.menu_restriction_tag.set(menu_restriction_tag)

        item.save()

    def load(self, data_list):
        updated_menuItems = []
        created_menuItems = []
        
        for obj in data_list:
            restaurant_name = obj.pop('restaurant_name')
            
            if restaurant_name == "Monarch Wings and Things":
                self.process_menu_item(obj, restaurant_name, updated_menuItems, created_menuItems)
            elif restaurant_name == "Monarch Butterflies":
                self.process_menu_item(obj, restaurant_name, updated_menuItems, created_menuItems)
        
        report = "--------------------------------------------------\n"
        report += "loadDefaultMenuItem Report\n"
        report += "--------------------------------------------------\n"

        if created_menuItems:
            report += "CREATED | These restaurants added new menu items to their menu:\n"
            for item_info in created_menuItems:
                item_name, restaurant_id = item_info.split(" -> ")
                restaurant_name = Restaurant.objects.get(pk=restaurant_id).name
                report += f"- {item_name} -> {restaurant_name}\n"

        if updated_menuItems:
            report += "UPDATED | These menu items were updated:\n"
            for item_info in updated_menuItems:
                item_name, restaurant_id = item_info.split(" -> ")
                restaurant_name = Restaurant.objects.get(pk=restaurant_id).name
                report += f"- {item_name} -> {restaurant_name}\n"

        # Print or log the report
        print(report)

