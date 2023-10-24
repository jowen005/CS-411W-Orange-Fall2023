from restaurants.models import RestTag,FoodTypeTag,CookStyleTag,TasteTag,AllergyTag,IngredientTag,RestrictionTag
  
from lcc_project.commands.load import LoadCommand, add_file_path

@add_file_path
class Command(LoadCommand):
    help = 'load menu item tag definitions from menutags.json.  [optional] specify -f to provide an alterintive tags.json file.'
    DEFAULT_JSON_PATH = 'json_files/menutags.json'
    
    def load(self, data_list):
        #opening menu tag file to read
        TAGS = data_list
              
        #clearing the tag tables before load, don't want a evergrownig table of duplicates! --- checking against database instead
        #FoodTypeTag.objects.all().delete()

        PresentRestTags = list(RestTag.objects.values_list('title',flat=True))
        PresentFoodTags = list(FoodTypeTag.objects.values_list('title',flat=True))
        PresentCookStyleTags = list(CookStyleTag.objects.values_list('title',flat=True))
        PresentAllergyTags = list(AllergyTag.objects.values_list('title',flat=True))
        PresentTasteTags = list(TasteTag.objects.values_list('title',flat=True))
        PresentRestrictionTags = list(RestrictionTag.objects.values_list('title',flat=True))
        PresentIngredientTags = list(IngredientTag.objects.values_list('title',flat=True))
        
        elementsEvaluated = 0
        newRestTags = 0
        newFoodTags = 0
        newCookTags = 0
        newAlleTags = 0
        newTastTags = 0
        newRestrTags = 0
        newIngrTags = 0

        #TO-DO should probably compair the database before and after instead of using a counter just to be sure they were actually added.
        for el in TAGS['RestTag']:
            elementsEvaluated += 1
            if not(el in PresentRestTags):
                newRestTags += 1
                RestTag.objects.create(title=str(el))
        for el in TAGS['FoodTypeTag']:
            elementsEvaluated += 1
            if not(el in PresentFoodTags):
                newFoodTags += 1
                FoodTypeTag.objects.create(title=str(el))
        for el in TAGS['CookStyleTag']:
            elementsEvaluated += 1
            if not(el in PresentCookStyleTags):
                newCookTags += 1
                CookStyleTag.objects.create(title=str(el))
        for el in TAGS['AllergyTag']:
            elementsEvaluated += 1
            if not(el in PresentAllergyTags):
                newAlleTags += 1
                AllergyTag.objects.create(title=str(el))
        for el in TAGS['TasteTag']:
            elementsEvaluated += 1
            if not(el in PresentTasteTags):
                newTastTags += 1
                TasteTag.objects.create(title=str(el))
        for el in TAGS['RestrictionTag']:
            elementsEvaluated += 1
            if not(el in PresentRestrictionTags):
                newRestrTags += 1
                RestrictionTag.objects.create(title=str(el))
        for el in TAGS['IngredientTag']:
            elementsEvaluated += 1
            if not(el in PresentIngredientTags):
                newIngrTags += 1
                IngredientTag.objects.create(title=str(el))

        print("-"*50)
        print("loadMenuTags Report")
        print("-"*50)

        print(str(elementsEvaluated) + " elements evaluated.")
        print("\t" + str(newRestTags) + " new restaurant  tags added.")
        print("\t" + str(newFoodTags) + " new food        tags added.")
        print("\t" + str(newCookTags) + " new cook style  tags added.")
        print("\t" + str(newAlleTags) + " new allergy     tags added.")
        print("\t" + str(newTastTags) + " new taste       tags added.")
        print("\t" + str(newRestrTags) + " new restriction tags added.")
        print("\t" + str(newIngrTags) + " new ingredient  tags added.")