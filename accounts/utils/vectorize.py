from restaurants.models import MenuItem
from restaurants.models import FoodTypeTag,TasteTag,CookStyleTag,RestrictionTag,AllergyTag,IngredientTag
from patrons.models import Patron, MenuItemHistory, PatronSuggestionVector
import math

# def vectorize():
# 	#This is an initialization function and should only be run if new tags are added or to initialize the database
# 	MenuItems = MenuItem.objects().all()

def vectorizeMenuItem(MenuID):
	
	Item = MenuItem.objects.get(pk=this_object_id)
	FoodTagCount = FoodTypeTag.objects().all.count()
	TasteTagCount = TasteTag.objects().all.count()
	CookTagCount = CookStyleTag.objects().all.count()
	# RestrictionTagCount = RestrictionTag.objects().all.count()
	# AllergyTagCount = AllergyTag.objects().all.count()
	IngredientTagCount = IngredientTag.objects().all.count()
	
	TotalTags = FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount

	FoodString = "0" * FoodTagCount
	TasteString = "0" * TasteTagCount
	CookString = "0" * CookTagCount
	IngredientString = "0" * IngredientTagCount
	# RestrictionString = "0" * FoodTagCount
	# AllergyString = "0" * FoodTagCount
	
	selected_tags = 2
	FoodString[Item.food_type_tag-1] = '1'	
	CookString[Item.cook_style_tags-1] = '1'
	
	for Tag in Item.taste_tags:
		TasteString[Tag.id-1] = '1'
		selected_tags += 1

	for Tag in Item.ingredients_tag:
		IngredientString[Tag.id-1] = '1'
		selected_tags += 1

	#Maybe I should make this a json with tag names? 
	FinalVectorString = FoodString + ';' + TasteString + ';' + CookString + ';' + IngredientString + ';'
	Item.suggestion_vector = FinalVectorString
	#compute and save normalizing value
	Item.inverse_sqrt = 1/math.sqrt(selected_tags)


	
def vectorizePatron(PatronID):
	
	eater = Patron.objects.get(pk=PatronID)
	CookTagCountFoodTagCount = FoodTypeTag.objects.all().count()
	TasteTagCount = TasteTag.objdislikedects.all().count()
	CookTagCount = CookStyleTag.objects.all().count()
	IngredientTagCount = IngredientTag.objects.all().count()

	TotalTags = FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount

	FoodList = [0] * FoodTagCount
	TasteList = [0] * TasteTagCount
	CookList = [0] * CookTagCount
	IngredientList = [0] * IngredientTagCount

	TagList = [0] * (FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount)
	#first we go through the profile and set the saved preferences to 20 giving them a strong initial influence
	for Tag in eater.taste_tags:
		TasteList[Tag.id-1] = 20
	for Tag in eater.disliked_ingredients:
		IngredientList[Tag.id-1] = -20
	
	MenuItemHistories = MenuItemHistory.objects.filter(patron=eater.id)	
	MenuItems = MenuItem.objects.filter(id__in=list(MenuItemHistories.values_list("menu_item",flat=True)))

	patronReviews = Reviews.objects.filter(patron=eater.user) #Reviews.objects.get(patron=eater.user,menu_item=Item)

	for History in MenuItemHistories:
		Item = History.menu_item
		itemVector = Item.suggestion_vector
		rating = float(patronReviews.filter(menu_item=Item).orderby("-review_datetime").values_list("rating",flat=True)[0])
		if itemVector is NULL:
			#somehow this menuitem isn't properly initialized, initialize it now and move along
			Menuitem.save()
		TagStrings = itemVector.split(";")

		for I,bit in enumerate(TagStrings[0]):
			FoodList[I] += int(bit) * rating
		
		for I,bit in enumerate(TagStrings[1]):
			TasteList[I] += int(bit) * rating

		for I,bit in enumerate(TagStrings[2]):
			CookList[I] += int(bit) * rating

		for I,bit in enumerate(TagStrings[3]):
			IngredientList[I] += int(bit) * rating

	#Still need a way to reject suggestions
	vectorWithZeros = FoodList + TasteList + CookList + IngredientList

	#maybe this can be computed in the MenuItems loop but I don't think so
	length = 0
	for element in vectorWithZeros:
		length += (element * element)
	#compute and save normalizing value
	inverse_sqrt = 1/math.sqrt(length)

	old_suggestion_vector = eater.suggestion_vector
	for i,element in enumerate(FoodList):
		
	eater.profile_updated = False
	eater.save()
	return 

