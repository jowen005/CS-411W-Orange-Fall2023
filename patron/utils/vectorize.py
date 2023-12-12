from restaurants.models import MenuItem
from restaurants.models import FoodTypeTag,TasteTag,CookStyleTag,RestrictionTag,AllergyTag,IngredientTag
from patron.models import Patron, MenuItemHistory, PatronSuggestionVector
from feedback.models import Reviews
import math

def vectorizePatron(PatronID):
	print("Vectorizing")
	eater = Patron.objects.get(pk=PatronID)
	FoodTagCount = FoodTypeTag.objects.all().count()
	TasteTagCount = TasteTag.objects.all().count()
	CookTagCount = CookStyleTag.objects.all().count()
	IngredientTagCount = IngredientTag.objects.all().count()

	TotalTags = FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount

	FoodList = [0] * FoodTagCount
	TasteList = [0] * TasteTagCount
	CookList = [0] * CookTagCount
	IngredientList = [0] * IngredientTagCount

	TagList = [0] * (FoodTagCount + TasteTagCount + CookTagCount + IngredientTagCount)
	#first we go through the profile and set the saved preferences to 20 giving them a strong initial influence
	#print("LOOK HERE ===========================================================================")
	#print(eater.patron_taste_tag.values_list())
	for Tag,name in eater.patron_taste_tag.values_list():
		#print("tag: " + name + ", id: " + str(Tag))
		TasteList[Tag-1] = 20
	for Tag,name in eater.disliked_ingredients.values_list():
		IngredientList[Tag-1] = -20
	
	MenuItemHistories = MenuItemHistory.objects.filter(patron=eater.id)	
	MenuItems = MenuItem.objects.filter(id__in=list(MenuItemHistories.values_list("menu_item",flat=True)))

	patronReviews = Reviews.objects.filter(patron=eater.user) #Reviews.objects.get(patron=eater.user,menu_item=Item)

	for History in MenuItemHistories:
		Item = History.menu_item
		itemVector = str(Item.suggestion_vector)
		rating = float(patronReviews.filter(menu_item=Item).orderby("-review_datetime").values_list("rating",flat=True)[0])
		if itemVector is None:
			#somehow this menuitem isn't properly initialized, initialize it now and move along
			Item.save()
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

	print(PatronID)
	suggestion_vector = PatronSuggestionVector.objects.filter(patron_id=PatronID)

	for i,element in enumerate(TasteList):
		if (element == 0):
			try:
				#if element is zero and the suggestion_vector is not zero set it to be zero and move along
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
				PatronSuggestionVector.objects.create(tag_id=i+1,tag_table="TasteTag",rating=element * inverse_sqrt,patron_id=PatronID)
				#vectorElement.save()
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
				PatronSuggestionVector.objects.create(tag_id=i+1,tag_table="CookTag",rating=element * inverse_sqrt,patron_id=PatronID)
				#vectorElement.save()
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
				PatronSuggestionVector.objects.create(tag_id=i+1,tag_table="FoodTag",rating=element * inverse_sqrt,patron_id=PatronID)
				#vectorElement.save()
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
				PatronSuggestionVector.objects.create(tag_id=i+1,tag_table="IngredientTag",rating=element * inverse_sqrt,patron_id=PatronID)
				#vectorElement.save()
			except (PatronSuggestionVector.MultipleObjectsReturned):
				print(f"Multiple enteries for tag_id: {i} in the IngredientTag table exist.")
				print("Something has gone terribly wrong and the database needs rebuilt.")

	eater.profile_updated = False
	eater.save()
	return 

