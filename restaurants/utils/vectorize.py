from restaurants.models import MenuItem
from restaurants.models import FoodTypeTag,TasteTag,CookStyleTag,RestrictionTag,AllergyTag,IngredientTag

# def vectorize():
# 	#This is an initialization function and should only be run if new tags are added or to initialize the database
# 	MenuItems = MenuItem.objects().all()

def vectorizeOne(MenuID):
	
	Item = MenuItem.objects.get(pk=this_object_id)
	FoodTagCount = FoodTypeTag.objects().all.count()
	TasteTagCount = TasteTag.objects().all.count()
	CookTagCount = CookStyleTag.objects().all.count()
	RestrictionTagCount = RestrictionTag.objects().all.count()
	AllergyTagCount = AllergyTag.objects().all.count()
	IngredientTagCount = IngredientTag.objects().all.count()
	
	TotalTags = FoodTagCount + TasteTagCount + CookTagCount + RestrictionTagCount + AllergyTagCount + IngredientTagCount

	FoodString = "0" * FoodTagCount
	TasteString = "0" * FoodTagCount
	CookString = "0" * FoodTagCount
	RestrictionString = "0" * FoodTagCount
	AllergyString = "0" * FoodTagCount
	IngredientString = "0" * FoodTagCount


	selected_tags = 2
	FoodString[Item.food_type_tag-1] = '1'
	
	for Tag in Item.taste_tags:
		TasteString[Tag.id-1] = '1'
		selected_tags += 1
	
	CookString[Item.cook_style_tags-1] = '1'

	for Tag in Item.menu_restriction_tag:
		RestrictionString[Tag.id-1] = '1'
		selected_tags += 1

	for Tag in Item.menu_allergy_tag:
		AllergyString[Tag.id-1] = '1'
		selected_tags += 1

	for Tag in Item.ingredients_tag:
		IngredientString[Tag.id-1] = '1'
		selected_tags += 1

	FinalVectorString = FoodString + TasteString + CookString + RestrictionString + AllergyString + IngredientString
	Item.suggestion_vector = FinalVectorString
	#compute and save normalizing value
	Item.inverse_sqrt = 1/math.sqrt(selected_tags)

	# food_type_tag = models.ForeignKey(FoodTypeTag, on_delete=models.SET_NULL, null=True)
    # taste_tags = models.ManyToManyField(TasteTag)
    # cook_style_tags = models.ForeignKey(CookStyleTag, on_delete=models.SET_NULL, null=True)
    # menu_restriction_tag = models.ManyToManyField(RestrictionTag)
    # menu_allergy_tag = models.ManyToManyField(AllergyTag)
    # ingredients_tag = models.ManyToManyField(IngredientTag)

	
