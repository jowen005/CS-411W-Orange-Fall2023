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

# Restaurants
## Rest Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/resttags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/resttags/ --> adds a tag
* Input: -
* Ouput: id, title

GET: restaurants/resttags/<int:id>/ --> retrieves a specific tag
* Input: -
* Ouput: id, title

PUT: restaurants/resttags/<int:id>/ --> updates a specific tag
* Input: title
* Ouput: id, title

DEL: restaurants/resttags/<int:id>/ --> deletes a specific tag
* Input: -
* Ouput: status204 if successful, "detail": "Not found." if not

## Food Type Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/foodtypetags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/foodtypetags/ --> adds a tag
* Input: -
* Ouput: id, title

GET: restaurants/foodtypetags/<int:id>/ --> retrieves a specific tag
* Input: -
* Ouput: id, title

PUT: restaurants/foodtypetags/<int:id>/ --> updates a specific tag
* Input: title
* Ouput: id, title

DEL: restaurants/foodtypetags/<int:id>/ --> deletes a specific tag
* Input: -
* Ouput: status204 if successful, "detail": "Not found." if not


## Cook Style Tags --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/cookstyletags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/cookstyletags/ --> adds a tag
* Input: -
* Ouput: id, title

GET: restaurants/cookstyletags/<int:id>/ --> retrieves a specific tag
* Input: -
* Ouput: id, title

PUT: restaurants/cookstyletags/<int:id>/ --> updates a specific tag
* Input: title
* Ouput: id, title

DEL: restaurants/cookstyletags/<int:id>/ --> deletes a specific tag
* Input: -
* Ouput: status204 if successful, "detail": "Not found." if not


## Taste Tags --- --- AdminAuth(All), RestAuth(GET), PatronAuth(GET)
GET: restaurants/tastetags/ --> lists all tags
* Input: -
* Output: {id, title}, {id, title}, ...

POST: restaurants/tastetags/ --> adds a tag
* Input: -
* Ouput: id, title

GET: restaurants/tastetags/<int:id>/ --> retrieves a specific tag
* Input: -
* Ouput: id, title

PUT: restaurants/tastetags/<int:id>/ --> updates a specific tag
* Input: title
* Ouput: id, title

DEL: restaurants/tastetags/<int:id>/ --> deletes a specific tag
* Input: -
* Ouput: status204 if successful, "detail": "Not found." if not