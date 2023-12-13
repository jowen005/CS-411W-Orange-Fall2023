# WITH Docker
## General Docker Commands
* **docker-compose up** --> starts up all containers in project with terminal display
  * **docker-compose up -d** --> starts up all containers in project without terminal display (detached mode)
* **docker-compose down** --> shuts down all containers in project

* **docker exec -it cs-411w-orange-fall2023-django-1 bash** --> opens shell inside django server container
  * **python3 manage.py migrate** ---> Make sure db is up to date
  * **python3 manage.py createsuperuser** ---> Creates a superuser (admin)
  * **exit** --> exits django shell

* **docker compose build** --> Rebuilds django container (use when requirements.txt is updated)

## Populating the Database (All within Django Container)
* **python3 manage.py init** --> runs a series of default load commands that initializes the database

* **python3 manage.py addRestaurants _int_** --> randomly generates and loads a specified number of restaurants
* **python3 manage.py addMenuItems _int_** --> randomly generates and loads a specified number of menu items
* **python3 manage.py addPatrons _int_** --> randomly generates and loads a specified number of patrons

* **python3 manage.py simulate** --> Runs a simulation with the following specifications (NOTE: would suggest running a hard reset before using)
  * If no analytics in database (simulate has not been run), generates patronTraffic, restaurantTraffic, and analytics for the past 7 days. It then generates patronTraffic, restaurantTraffic, analytics, and trends for today.
  * If analytics are in database (simulate has been run), it generates patronTraffic, restaurantTraffic, analytics, and trends for today.
  * FLAGS
    * **--soft_reset** --> deletes all traffic, analytics, and trends for TODAY
    * **--hard_reset** --> deletes all traffic for the LAST 8 DAYS and ALL analytics/trends
    * **-n _int_** --> specifies a specific number of searches per user

* **python3 manage.py generatePatronTraffic _patronEmail_** --> randomly simulates patron traffic with 1 search (default) or a specified number of times (-n _int_). Simulated actions include searching, bookmarking, submitting feedback, and adding to menu item history.


* **python3 manage.py updateFields** --> updates objects in older databases to be consistent with newer updates.

* **python3 manage.py manualAnalytics** --> manually triggers the execution of all analytic algorithms

* **python3 manage.py manualTrends** --> manually triggers the execution of all trend algorithms



## For Backend Devs Only
* Use **docker-compose up** in dev branch
* Use **docker-compose -f docker-compose.yml up** in main branch (ignores override.yml)

Note:
* When running in main branch:
 * Use **docker-compose -f docker-compose.yml up**
 * This excludes the override file, defaulting to the main branch database
 * Make sure your secret_path.json refers to 'secrets.json'
* When running in dev branch:
 * Use **docker-compose up**
 * This uses the override file to override the database used for development
* Make sure your secret_path.json refers to 'secrets_dev.json'

Note: See NOTES_DOCKER.md for more information

## Populating the Database (IN DETAIL)
* **python3 manage.py init** --> runs a series of default load commands that initializes the database
  * **python3 manage.py loadMenuTags** --> loads the default menu tags
  * **python3 manage.py loadDefaultAccounts** --> loads the default patron, restaurant, and admin accounts
  * **python3 manage.py loadDefaultPatrons** --> loads the default patron profiles
  * **python3 manage.py loadDefaultRestaurants** --> loads the default restaurants
  * **python3 manage.py loadDefaultMenuItems** --> loads default menu items

* **python3 manage.py addRestaurants _int_** --> randomly generates and loads a specified number of restaurants 
  * **python3 manage.py generateRestaurants _int_** --> generates randomized restaurant information into restaurantBuffer.json
  * **python3 manage.py loadRestaurants** --> loads restaurant json objects from restaurantBuffer.json (default) or a specified file (-f=_filepath_)

* **python3 manage.py addMenuItems _int_** --> randomly generates and loads a specified number of menu items
  * **python3 manage.py generateMenuItems _int_** --> generates randomized menu item information into menuItemBuffer.json
  * **python3 manage.py loadMenuItem** --> loads menu item json objects from menuItemBuffer.json (default) or a specified file (-f=_filepath_)

* **python3 manage.py addPatrons _int_** --> randomly generates and loads a specified number of patrons
  * **python3 manage.py generatePatrons _int_** --> generates randomized patron information into patronBuffer.json
  * **python3 manage.py loadPatrons** --> loads patron json objects from patronBuffer.json (default) or a specified file (-f=_filepath_)

* **python3 manage.py generatePatronTraffic _patronEmail_** --> randomly simulates patron traffic with 1 search (default) or a specified number of times (-n _int_). Simulated actions include searching, bookmarking, submitting feedback, and adding to menu item history.

* **python3 manage.py updateFields** --> updates objects in older databases to be consistent with newer updates.
  * **python3 manage.py updateCalorieLevels** --> manually updates the calorie levels of all menu items, patrons, and searches.
  * **python3 manage.py updateFeedback** --> manually updates the patron names associated with all reviews.
  * **python3 manage.py updateVectors** --> manually updates the tag vectors of menu items and patrons.

* **python3 manage.py manualAnalytics** --> manually triggers the execution of all analytic algorithms

* **python3 manage.py manualTrends** --> manuall triggers the execution of all trend algorithms



## Server pushes with Docker (Foster)
* **docker login -u wtfoster2**
* **docker tag __imageid__ wtfoster2/cs411wforang:__tag__**
* **docker push wtfoster2/cs411wforang:__tag__**
* **docker logout**




# WITHOUT Docker (DEPRECATED)
## Virtual Environments
* **python3 -m venv .env** ---> Creates the - .env virtual environment
* **source .env/bin/activate** ---> Activates the virtual environment
* **deactivate** ---> Deactivates the virtual environment

## Common Commands
* **source .env/bin/activate** ---> Activates the virtual environment
* **python3 manage.py runserver** ---> Views the project in its current state
* **python3 manage.py migrate** ---> Make sure db is up to date
* **python3 manage.py createsuperuser** ---> Creates a superuser (admin)
* **python3 manage.py test** ---> Runs all backend tests
* **python3 -Wa manage.py test** ---> Runs all backend tests with outputting warnings
* **python3 manage.py test -v1** ---> v1, v2, v3, or v4 makes output more descriptive 