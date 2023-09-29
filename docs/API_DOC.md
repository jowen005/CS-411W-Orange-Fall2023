# Accounts (/auth/)
## Login --- Patron(POST), Rest(POST), Admin(POST)
POST: /auth/login/ --> Creates and returns access an refresh tokens
* Input: email, password
* Output: message, user_type, tokens{access, refresh}

## SignUp --- Patron(POST), Rest(POST)
POST: /auth/signup/<str:user_type>/
* Input: email, username, password
* Output: message, content{email, username, user_type}

* Admin cannot be created using API

## JWT (Json Web Tokens) --- Access to Anyone
POST: /auth/jwt/create/ --> creates and returns an access and refresh token
* Input: email, password
* Output: refresh, access

POST: /auth/jwt/refresh/ --> creates and returns a new access token
* Input: refresh
* Output: access

POST: /auth/jwt/verify/ --> verifies a token
* Input: token
* Output: nothing if valid, message if not

# Restaurants (/restaurants/)
## Restaurants --- RestAuth(All) && User Owns 'restaurant_id'
GET: restaurants/ --> lists all restaurants owned by user
* Input: -
* Output: List of restaurants

POST: restaurants/ --> adds a new restaurant owned by user
* Input: name, rating, tags[tag1,tag2,...], price_level, phone_number, website, 
                    street_name, city, state, zip_code, mon_open, mon_close,
                    tue_open, tue_close, wed_open, wed_close, thu_open, thu_close
                    fri_open, fri_close, sat_open, sat_close, sun_open, sun_close
* Output: id, owner, name, rating, tags[tag1,tag2,...], price_level, phone_number, website, 
                    street_name, city, state, zip_code, mon_open, mon_close,
                    tue_open, tue_close, wed_open, wed_close, thu_open, thu_close
                    fri_open, fri_close, sat_open, sat_close, sun_open, sun_close

GET: restaurants/<int:restaurant_id>/ --> retrieves a specific restaurant owned by user
* Input: -
* Output: id, owner, name, rating, tags[tag1,tag2,...], price_level, phone_number, website, 
                    street_name, city, state, zip_code, mon_open, mon_close,
                    tue_open, tue_close, wed_open, wed_close, thu_open, thu_close
                    fri_open, fri_close, sat_open, sat_close, sun_open, sun_close

PUT: restaurants/<int:restaurant_id>/ --> updates a specific restaurant owned by user
* Input: name, rating, tags[tag1,tag2,...], price_level, phone_number, website, 
                    street_name, city, state, zip_code, mon_open, mon_close,
                    tue_open, tue_close, wed_open, wed_close, thu_open, thu_close
                    fri_open, fri_close, sat_open, sat_close, sun_open, sun_close
* Output: id, owner, name, rating, tags[tag1,tag2,...], price_level, phone_number, website, 
                    street_name, city, state, zip_code, mon_open, mon_close,
                    tue_open, tue_close, wed_open, wed_close, thu_open, thu_close
                    fri_open, fri_close, sat_open, sat_close, sun_open, sun_close

DEL: restaurants/<int:restaurant_id>/ --> deletes a specific restaurant owned by user
* Input: -
* Output: (status204) if successful --- ("detail": "Not found.") if not

## Menu Items --- RestAuth(All) && User Owns 'restaurant_id' && 'item_id' belongs to 'restaurant_id
GET: restaurants/<int:restaurant_id>/menuitems/ --> lists all menu items belonging to 'restaurant_id'
* Input: -
* Output: List of Menu Items belonging to 'restaurant_id'

POST: restaurants/<int:restaurant_id>/menuitems/ --> adds a menu item belonging to 'restaurant_id'
* Input: item_name, average_rating, price, calories, food_type_tag, taste_tags[tag1,tag2,...], 
                    cook_style_tags, menu_restriction_tag[tag1,tag2,...], menu_allergy_tag[tag1,tag2,...],
                    ingredients_tag[tag1,tag2,...], time_of_day_available, is_modifiable
* Output: id, restaurant, item_name, average_rating, price, calories, food_type_tag, taste_tags[tag1,tag2,...], 
                    cook_style_tags, menu_restriction_tag[tag1,tag2,...], menu_allergy_tag[tag1,tag2,...],
                    ingredients_tag[tag1,tag2,...], time_of_day_available, is_modifiable

GET: restaurants/<int:restaurant_id>/menuitems/<int:item_id>/ --> retrieves a specific menu items belonging to 'restaurant_id'
* Input: -
* Output: id, restaurant, item_name, average_rating, price, calories, food_type_tag, taste_tags[tag1,tag2,...], 
                    cook_style_tags, menu_restriction_tag[tag1,tag2,...], menu_allergy_tag[tag1,tag2,...],
                    ingredients_tag[tag1,tag2,...], time_of_day_available, is_modifiable

PUT: restaurants/<int:restaurant_id>/menuitems/<int:item_id>/ --> updates a specific menu items belonging to 'restaurant_id'
* Input: item_name, average_rating, price, calories, food_type_tag, taste_tags[tag1,tag2,...], 
                    cook_style_tags, menu_restriction_tag[tag1,tag2,...], menu_allergy_tag[tag1,tag2,...],
                    ingredients_tag[tag1,tag2,...], time_of_day_available, is_modifiable
* Output: id, restaurant, item_name, average_rating, price, calories, food_type_tag, taste_tags[tag1,tag2,...], 
                    cook_style_tags, menu_restriction_tag[tag1,tag2,...], menu_allergy_tag[tag1,tag2,...],
                    ingredients_tag[tag1,tag2,...], time_of_day_available, is_modifiable

DEL: restaurants/<int:restaurant_id>/menuitems/<int:item_id>/ --> deletes a specific menu items belonging to 'restaurant_id'
* Input: -
* Output: status204 if successful, "detail": "Not found." if not

## Rest Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/resttags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/resttags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/resttags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/resttags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/resttags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not

## Food Type Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/foodtypetags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/foodtypetags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/foodtypetags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/foodtypetags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/foodtypetags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not


## Cook Style Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/cookstyletags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/cookstyletags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/cookstyletags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/cookstyletags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/cookstyletags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not


## Taste Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/tastetags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/tastetags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/tastetags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/tastetags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/tastetags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not

## Restriction Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/restrictiontags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/restrictiontags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/restrictiontags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/restrictiontags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/restrictiontags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not

## Allergy Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/allergytags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/allergytags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/allergytags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/allergytags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/allergytags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not

## Ingredient Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/ingredienttags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/ingredienttags/ --> adds a tag
* Input: title
* Output: id, title

GET: restaurants/ingredienttags/<int:id>/ --> retrieves a specific tag
* Input: -
* Output: id, title

PUT: restaurants/ingredienttags/<int:id>/ --> updates a specific tag
* Input: title
* Output: id, title

DEL: restaurants/ingredienttags/<int:id>/ --> deletes a specific tag
* Input: -
* Output: status204 if successful, "detail": "Not found." if not


# Patrons (/patrons/)
## Patrons --- PatronAuth(All) && User Owns 'patron_id'
GET: patrons/ --> lists the patron owned by user
* Input: -
* Output: List of patrons (will only be the ONE the user has access to)

POST: patrons/ --> creates a patron profile for the user (Only allowed one)
* Input: name, gender, price_preference, zipcode, patron_restriction_tag[tag1,tag2,...], 
                patron_allergy_tag[tag1,tag2,...], patron_taste_tag[tag1,tag2,...],
                dob, calorie_limit
                    
* Output: id, user, name, gender, price_preference, zipcode, patron_restriction_tag[tag1,tag2,...], 
                patron_allergy_tag[tag1,tag2,...], patron_taste_tag[tag1,tag2,...],
                dob, calorie_limit
GET: patrons/<int:patron_id>/ --> retrieves the specific patron profile the user has access to
* Input: -
* Output: id, user, name, gender, price_preference, zipcode, patron_restriction_tag[tag1,tag2,...], 
                patron_allergy_tag[tag1,tag2,...], patron_taste_tag[tag1,tag2,...],
                dob, calorie_limit

PUT: patrons/<int:patron_id>/ --> updates the user's patron profile
* Input: name, gender, price_preference, zipcode, patron_restriction_tag[tag1,tag2,...], 
                patron_allergy_tag[tag1,tag2,...], patron_taste_tag[tag1,tag2,...],
                dob, calorie_limit
* Output: id, user, name, gender, price_preference, zipcode, patron_restriction_tag[tag1,tag2,...], 
                patron_allergy_tag[tag1,tag2,...], patron_taste_tag[tag1,tag2,...],
                dob, calorie_limit

DEL: patrons/<int:patron_id>/ --> deletes a user's patron profile
* Input: -
* Output: (status204) if successful --- ("detail": "Not found.") if not

