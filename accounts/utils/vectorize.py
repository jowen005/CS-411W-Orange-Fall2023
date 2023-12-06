from restaurants.models import MenuItem
from restaurants.models import FoodTypeTag,TasteTag,CookStyleTag,RestrictionTag,AllergyTag,IngredientTag
from patron.models import Patron, MenuItemHistory, PatronSuggestionVector
import math

def vectorizeMenuItem(menu_item, tag_counts):
	Item = menu_item
	FoodTagCount = tag_counts['FoodTypeTag']
	TasteTagCount = tag_counts['TasteTag']
	CookTagCount = tag_counts['CookStyleTag']
	IngredientTagCount = tag_counts['IngredientTag']



	# Item = MenuItem.objects.get(pk=MenuID)
	# FoodTagCount = FoodTypeTag.objects().all.count()
	# TasteTagCount = TasteTag.objects().all.count()
	# CookTagCount = CookStyleTag.objects().all.count()
	# IngredientTagCount = IngredientTag.objects().all.count()
	# RestrictionTagCount = RestrictionTag.objects().all.count()
	# AllergyTagCount = AllergyTag.objects().all.count()
	
	
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
	Item.save()

	
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

	suggestion_vector = PatronSuggestionVector.object.filter(patron=PatronID)

	for i,element in enumerate(TasteList):
		if (element == 0):
			try:
				vectorElement = suggestion_vector.get(tag_table="TasteTag",tag_id=i+1)
				vectorElement.rating = 0
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				#nothing needs to be done, idk wy get doesn't just return null if no element matchs but I don't make the rules
				pass
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the TasteTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")
		else:
			try:
				vectorElement = suggestion_vector.get(tag_table="TasteTag",tag_id=i+1)
				vectorElement.rating = element * inverse_sqrt
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				vectorElement = PatronSuggestionVector(tag_id=i+1,tag_table="TasteTag",rating=element * inverse_sqrt,patron=PatronID)
				vectorElement.save()
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the TasteTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")

	for i,element in enumerate(CookList):
		if (element == 0):
			try:
				vectorElement = suggestion_vector.get(tag_table="CookStyle",tag_id=i+1)
				vectorElement.rating = 0
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				#nothing needs to be done, idk wy get doesn't just return null if no element matchs but I don't make the rules
				pass
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the CookTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")
		else:
			try:
				vectorElement = suggestion_vector.get(tag_table="CookTag",tag_id=i+1)
				vectorElement.rating = element * inverse_sqrt
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				vectorElement = PatronSuggestionVector(tag_id=i+1,tag_table="CookTag",rating=element * inverse_sqrt,patron=PatronID)
				vectorElement.save()
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the FoodTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")

	for i,element in enumerate(FoodList):
		if (element == 0):
			try:
				vectorElement = suggestion_vector.get(tag_table="FoodTag",tag_id=i+1)
				vectorElement.rating = 0
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				#nothing needs to be done, idk wy get doesn't just return null if no element matchs but I don't make the rules
				pass
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the FoodTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")
		else:
			try:
				vectorElement = suggestion_vector.get(tag_table="FoodTag",tag_id=i+1)
				vectorElement.rating = element * inverse_sqrt
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				vectorElement = PatronSuggestionVector(tag_id=i+1,tag_table="FoodTag",rating=element * inverse_sqrt,patron=PatronID)
				vectorElement.save()
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the FoodTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")

	for i,element in enumerate(IngredientList):
		if (element == 0):
			try:
				vectorElement = suggestion_vector.get(tag_table="IngredientTag",tag_id=i+1)
				vectorElement.rating = 0
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				#nothing needs to be done, idk wy get doesn't just return null if no element matchs but I don't make the rules
				pass
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the IngredientTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")
		else:
			try:
				vectorElement = suggestion_vector.get(tag_table="IngredientTag",tag_id=i+1)
				vectorElement.rating = element * inverse_sqrt
				vectorElement.save()
			except (PatronSuggestionVector.DoesNotExist):
				vectorElement = PatronSuggestionVector(tag_id=i+1,tag_table="IngredientTag",rating=element * inverse_sqrt,patron=PatronID)
				vectorElement.save()
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the IngredientTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")

	eater.profile_updated = False
	eater.save()
	return 

