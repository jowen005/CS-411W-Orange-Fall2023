
# FLOWS
## Everytime you make request:
1. Make a http header with request
   1. Key is "Authorization"
   2. Value is "Bearer *AccessToken*"

## LogIn Flow Steps
1. User inputs information
2. When they click login button, call 'localhost:8000/auth/login/' POST
3. If successful, the response will contain tokens and *user_type*
   1. Depending on user_type, navigate to appropriate page and pass *AccessToken*

## Signup Flow Steps
1. User inputs information
2. When they click submit button, call appropriate 'localhost:8000/auth/signup/<str:user_type>/' POST
3. If successful, the response will contain tokens
   1. If Rest, navigate to restaurant homepage and pass *AccessToken*
   2. If Patron, navigate to profile creation page and pass *AccessToken*
      1. User inputs information 
      2. When they click submit button, call 'localhost:8000/patrons/' POST
      3. If successful, navigate to patron homepage and pass *AccessToken*

## Tag Selection
1. List Tags using 'localhost:8000/restaurants/_tagtype_/' GET (LIST)
2. Display Title from the list of tags to be selected
3. Record IDs of tags that are selected
4. Use those selected IDs with the API you are trying to use (Patron Profile CRUD, Menu Item CRUD, etc)

## Restaurant Flow Steps
1. Upon entry of the Restaurant Homepage call 'localhost:8000/restaurants/' with GET (LIST)
   1. Display restaurants names in list
   2. Upon clicking a restaurant displayed, navigate to restaurant page, and pass *rest_id* and *AccessToken* to that page
      1. Upon entry to restaurant page, call 'localhost:8000/restaurants/*rest_id*' with GET (RETRIEVE)
         1. Also call 'localhost:8000/restaurants/*rest_id*/menuitems/' GET (LIST)
         2. Upon clicking on menu item, navigate to menu item page, and pass *rest_id* and *menu_item_id* and *AccessToken*
            1. Upon entry to menu item page, call 'localhost:8000/restaurants/*id*/menuitems/*menu_item_id*' GET (RETRIEVE)

# Patron Flow Steps
1. While on Patron Homepage, click on Preferences/Settings button to navigate to page passing *AccessToken*
2. Upon entry to settings page, call 'localhost:8000/patrons/' with GET (LIST)
   1. When you want to update information, call 'localhost:8000/patrons/<int:patron_id>/' with PUT (UPDATE)

# SITEMAPS
## Create Account
* Rest Signup (Tuan)
* Patron Signup (Lindsay) 
  * Patron Profile Creation (Lindsay)

## Login
* Login (Tuan)

## Patron Overview SiteMap
* *Homepage* (Kendra)
  * *Settings -> Settings Page*
  * Search -> Search Page
  * Meal History -> Meal History Page
  * Bookmark -> Bookmark Page
  * Suggestion Feed

* *Settings* (Kendra/Lindsay)
  * Display Profile Page
  * Edit Button -> Edit Profile Page

* *Editing Info* (Lindsay)
  * Update all information
  * Submit -> Settings


## Restaurant Overview SiteMap
* *Homepage* (Tuan)
  * Global Analytics (account-wide analytics and trends)
  * *List of Restaurants -> Rest Page* 

* *Restaurant Page* (Tuan)
  * *(Home)Profile Information for that restaurant*
    * Local Restaurant Analytics
  * *List of Menu Items -> MenuItem Page*

* *MenuItem Page* (Justin)
  * *(Home)Menu Item Information*
  * Menu Item Analytics

* *Admin* (Aaron)