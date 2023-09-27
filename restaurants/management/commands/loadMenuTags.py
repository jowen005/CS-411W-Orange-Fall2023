from restaurants.models import FoodTypeTag,CookStyleTag,TasteTag,Allergy_tag,IngredientsTag,Restriction_tag
  
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
        Allergy_tag.objects.all().delete()
        TasteTag.objects.all().delete()
        Restriction_tag.objects.all().delete()
        IngredientsTag.objects.all().delete()

        for el in TAGS['resttags']['FoodTypeTag']:
            FoodTypeTag.objects.create(title=str(el))
        for el in TAGS['resttags']['CookStyleTag']:
            CookStyleTag.objects.create(title=str(el))
        for el in TAGS['resttags']['Allergy_tag']:  
            Allergy_tag.objects.create(title=str(el))
        for el in TAGS['resttags']['TasteTag']:
            TasteTag.objects.create(title=str(el))
        for el in TAGS['resttags']['Restriction_tag']:
            Restriction_tag.objects.create(title=str(el))
        for el in TAGS['resttags']['IngredientsTag']:
            IngredientsTag.objects.create(title=str(el))