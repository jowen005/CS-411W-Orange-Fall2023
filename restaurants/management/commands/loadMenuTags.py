from restaurants.models import FoodTypeTag,CookStyleTag,TasteTag,AllergyTag,IngredientTag,RestrictionTag
  
from lcc_project.commands.load import LoadCommand, add_file_path

@add_file_path
class Command(LoadCommand):
    help = 'load menu item tag definitions from menutags.json.  [optional] specify -f to provide an alterintive tags.json file.'
    DEFAULT_JSON_PATH = 'json_files/menutags.json'
    
    def load(self, data_list):
        #opening menu tag file to read
        TAGS = data_list
              
        #clearing the tag tables before load, don't want a evergrownig table of duplicates!
        FoodTypeTag.objects.all().delete()
        CookStyleTag.objects.all().delete()
        AllergyTag.objects.all().delete()
        TasteTag.objects.all().delete()
        RestrictionTag.objects.all().delete()
        IngredientTag.objects.all().delete()

        for el in TAGS['resttags']['FoodTypeTag']:
            FoodTypeTag.objects.create(title=str(el))
        for el in TAGS['resttags']['CookStyleTag']:
            CookStyleTag.objects.create(title=str(el))
        for el in TAGS['resttags']['AllergyTag']:  
            AllergyTag.objects.create(title=str(el))
        for el in TAGS['resttags']['TasteTag']:
            TasteTag.objects.create(title=str(el))
        for el in TAGS['resttags']['RestrictionTag']:
            RestrictionTag.objects.create(title=str(el))
        for el in TAGS['resttags']['IngredientTag']:
            IngredientTag.objects.create(title=str(el))