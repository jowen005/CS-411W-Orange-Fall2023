# CS-411W-Orange-Fall2023
CS 411W Team Orange Project: LowCalChow
### This is the FOSTER Branch
# SECRET management
Create a secrets.json file in the main directory and fill out the file according to the instructions provided. This keeps all host-specific information on each computer. 

Note: because secrets.json is in the gitignore file, if you plan on working on multiple branches, the secrets.json file will be ignored and will stay static across all branchs. To fix this, you can create a secrets.json file for each branch following the convention secrets*.json and reference it at the beginning of settings.py. These will be ignored by git, just REMEMBER to change settings.py back to standard 'secrets.json' before merging with 'main'

# APPS:
* Accounts
  * User

* Restaurant    
  * Restaurant
  * RestTag
  * RestOpenHour
  * RestDataAPI

* Menu
  * MenuItems

* Patron
  * Patron
  * DRTag
  * PPTag
  * Search History
  * Bookmark
  * Meal History

* Feedback
  * Reviews
  * Ratings

* Analysis
  * Analytics
  * Trends

* APIScraper
