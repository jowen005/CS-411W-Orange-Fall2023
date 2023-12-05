from patron.models import Patron, PatronSuggestionVector
from restaurants.models import MenuItem
from accounts.utils.vectorize import vectorizePatron
from queue import PriorityQueue

def generateSuggestions(PatronID):
	patron = Patrons.objects.get(id=PatronID)
	if(patron.profile_updated):
		vectorizePatron(PatronID)
	
	allergys = patron.patron_allergy_tag.values_list("id",flat=True)
	MenuItems = MenuItem.objects.exclude(menu_allergy_tag__in = allergys)
	restrictions = patron.patron_restriction_tag.values_list("id",flat=True)
	MenuItems = MenuItems.filter(menu_restriction_tag__in = restrictions)
	patron_suggestion_vector = PatronSuggestionVector.objects.filter(patron = PatronID)

	TagsCount = FoodTypeTag.objects.all().count() + TasteTag.objdislikedects.all().count() + CookStyleTag.objects.all().count() + IngredientTag.objects.all().count()
	
	itemDictionary = PriorityQueue()
	#python's priority queue implementation has log(n) time complexity and since this list needs to be sorted anyway which sorts in nlog(n) time
	#doing the sort during the loop make the sort log(n!) which is < nlog(n)
	#[("FoodTag","FoodTag"), ("TasteTag","TasteTag"), ("CookStyle","CookStyle"), ("IngredientTag","IngredientTag")]
	for Item in MenuItems:
		itemVector = Item.suggestion_vector.split(';')
		vectorSum = 0
		#this loop takes the dotproduct between the menuItem's suggestion Vector and the patron's suggestion Vector
		for suggestion in patron_suggestion_vector:
			match(suggestion.tag_table):
				case "FoodTag":
					vectorSum += int(itemVector[0][suggestion.tag_id - 1] * Item.inverse_sqrt) * suggestion.rating
				case "TasteTag":
					vectorSum += int(itemVector[1][suggestion.tag_id - 1] * Item.inverse_sqrt) * suggestion.rating
				case "CookStyle":
					vectorSum += int(itemVector[2][suggestion.tag_id - 1] * Item.inverse_sqrt) * suggestion.rating
				case "IngredientTag":
					vectorSum += int(itemVector[3][suggestion.tag_id - 1] * Item.inverse_sqrt) * suggestion.rating
		#because some precision is lost when storing the suggestion vectors the values might be slightly above 1 or below -1 so we'll clip the values
		#the error will never be significant because our precision is about ±0.00000001
		if(vectorSum < -1):
			vectorSum = -1
		elif(vectorSum >1):
			vectorSum = 1
		#priority queue in python sorts least to most so we'll subtract the vectorSum from 1 and divide by 2 to restrict the domain to (0,1)
		vectorSum = 1 - vectorSum
		itemDictionary.put((vectorSum,Item.id))
	
	#because for some reason of ALL things the priorityqueue cant be cast to a list we do this
	results = []
	for i in range(itemDictionary.qsize):
		results.append(itemDictionary.get())
	return results