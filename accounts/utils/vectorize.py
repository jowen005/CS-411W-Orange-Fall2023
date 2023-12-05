from restaurants.models import MenuItem
from restaurants.models import FoodTypeTag,TasteTag,CookStyleTag,RestrictionTag,AllergyTag,IngredientTag
from patrons.models import Patron
from patrons.models import MenuItemHistory
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
	# RestrictionString = "0" * FoodTagCount
	# AllergyString = "0" * FoodTagCount
	IngredientString = "0" * IngredientTagCount


	selected_tags = 2
	FoodString[Item.food_type_tag-1] = '1'	
	CookString[Item.cook_style_tags-1] = '1'
	
	for Tag in Item.taste_tags:
		TasteString[Tag.id-1] = '1'
		selected_tags += 1

	# for Tag in Item.menu_restriction_tag:
	# 	RestrictionString[Tag.id-1] = '1'
	# 	selected_tags += 1

	# for Tag in Item.menu_allergy_tag:
	# 	AllergyString[Tag.id-1] = '1'
	# 	selected_tags += 1

	for Tag in Item.ingredients_tag:
		IngredientString[Tag.id-1] = '1'
		selected_tags += 1

	FinalVectorString = FoodString + TasteString + CookString + IngredientString
	Item.suggestion_vector = FinalVectorString
	#compute and save normalizing value
	Item.inverse_sqrt = 1/math.sqrt(selected_tags)
	
def vectorizePatron(PatronID):
	
	eater = Patron.objects.get(pk=this_object_id)
	CookTagCountFoodTagCount = FoodTypeTag.objects.all().count()
	TasteTagCount = TasteTag.objdislikedects.all().count()
	CookTagCount = CookStyleTag.objects.all().count()
	IngredientTagCount = IngredientTag.objects.all().count()

	TotalTags = FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount

	MenuItemHistories = MenuItemHistory.objects.filter(patron=eater.id)	
	MenuItems = MenuItem.objects.filter(id__in=list(MenuItemHistories.values_list(menu_item,flat=true)))

	FoodList = [0] * FoodTagCount
	TasteList = [0] * TasteTagCount
	CookList = [0] * CookTagCount
	IngredientList = [0] * IngredientTagCount

	#first we go through the profile and set the saved preferences to 20 giving them a strong initial influence
	for Tag in eater.taste_tags:
		TasteList[Tag.id-1] = 20
	for Tag in eater.disliked_ingredients:
		IngredientList[Tag.id-1] = -20
	
	for Item in MenuItems:
		V = MenuItem.suggestion_vector
		if V is NULL:
			#somehow this menuitem isn't properly initialized, initialize it now and move along
			Menuitem.save()
		FoodString = V[0:FoodTagCount+1]
		TasteString = V[FoodTagCount+1:TasteTagCount+FoodTagCount+1]
		CookString = V[TasteTagCount+FoodTagCount+1:CookTagCount+TasteTagCount+FoodTagCount+1]
		IngredientString = V[CookTagCount+TasteTagCount+FoodTagCount+1:]

		for bit,I in FoodString:
			FoodList[I] += int(bit) * (V.review - 2.5)
		
		for bit,I in TasteString:
			TasteList[I] += int(bit) * (V.review - 2.5)

		for bit,I in CookString:
			CookList[I] += int(bit) * (V.review - 2.5)

		for bit,I in IngredientString:
			IngredientList[I] += int(bit) * (V.review - 2.5)

	#Still need a way to reject suggestions
	vectorWithZeros = FoodList + TasteList + CookList + IngredientList

	#maybe this can be computed in the MenuItems loop but I don't think so
	length = 0
	for element in vectorWithZeros:
		length += (element * element)
	#compute and save normalizing value
	inverse_sqrt = 1/math.sqrt(length)






	#none of this crap shoud be used
	FinalVectorString = ""
	#this loop trims out the zero values to reduce the size on the database
	for element,i in vectorWithZeros:
		#I'm going to round here and lose some precision but not too much and there should still be enough for the suggestion feed
		if(element != 0):
			FinalVectorString += str(i) + ":" + str(math.round((element * inverse_sqrt),5)) + ";"


	FinalVectorString = FoodString + TasteString + CookString + RestrictionString + AllergyString + IngredientString
	Item.suggestion_vector = FinalVectorString
	#eater.inverse_sqrt = invSqr

	# food_type_tag = models.ForeignKey(FoodTypeTag, on_delete=models.SET_NULL, null=True)
    # taste_tags = models.ManyToManyField(TasteTag)
    # cook_style_tags = models.ForeignKey(CookStyleTag, on_delete=models.SET_NULL, null=True)
    # menu_restriction_tag = models.ManyToManyField(RestrictionTag)
    # menu_allergy_tag = models.ManyToManyField(AllergyTag)
    # ingredients_tag = models.ManyToManyField(IngredientTag)

