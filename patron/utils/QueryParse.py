def QueryParser(query_string:str):
	query_string = query_string.lower()
	
	allergyTags = Allergy_Tags.objects.values_list('title',flat=true)
	for tag in allergyTags:
		#we don't to match with tags that are found inside other words so suround the search with spaces
		tagF = ' ' + tag + ' '
		#if no instances of tag are found remove from allergyTags list
		if(query_string.count(tagF) == 0):
			allergyTags.remove(tag)
		else:
			#remove all instances of the tag.  This cleans the string up of accounted for tags and slightly speeds up the next count operation
			query_string.replace(tagF, ' ')
			
	ingredientTags = Ingredient_Tags.objects.values_list('title',flat=true)
	for tag in ingredientTags:
		tagF = ' -' + tag + ' '
		if(query_string.count(tagF) == 0):
			ingredientTags.remove(tag)
		else:
			query_string.replace(tagF, ' ')		
			
	TasteTags = Taste_Tags.objects.values_list('title',flat=true)
	for tag in TasteTags:
		tagF = ' ' + tag + ' '
		if(query_string.count(tagF) == 0):
			TasteTags.remove(tag)
		else:
			query_string.replace(tagF, ' ')
			
	RestrictionTags = Restriction_Tags.objects.values_list('title',flat=true)
	for tag in RestrictionTags:
		tagF = ' ' + tag + ' '
		if(query_string.count(tagF) == 0):
			RestrictionTags.remove(tag)
		else:
			query_string.replace(tagF, ' ')
			
	StyleTags = Style_Tags.objects.values_list('title',flat=true)
	for tag in StyleTags:
		tagF = ' ' + tag + ' '
		if(query_string.count(tagF) == 0):
			StyleTags.remove(tag)
		else:
			query_string.replace(tagF, ' ')

	#all pre defined tags should be removed from the string now
	query_string.replace(' - ', ' ')
	query_string = query_string.strip()
	
	#This is the quick and sloppy way to do his, doing this right is going to require a regular expression. I beg forgiveness  for my sins
	#regular expression procedure:
	#find start of the calorie sub string  DONE
	#find first occurance of character other than [' ',':','(','\d',')']
	#create substring from calorieStart to first occurance -1
	#remove whitespace
	calorieStart = query_string.find('calories:')
	if (calorieStart > -1):
		#is this a predefined tupple? 
		if (query_string[calorieStart+9] == '('):
			delimiter = query_string.find(':',start=calorieStart+9)
			closer = query_string.find(')',start=calorieStart+9)
			if(delimiter > -1):
				minCal = query_string[calorieStart+10:delimiter-1]
				if(closer > -1):
					maxCal = query_string[delimiter+1:closer-1]
				else: #this is a bad query_string
					#dances with wolves hedows dfwqfwefaoisojfswieoru
			else: #this is a bad query_string
			
		else:#only max is defined
			