# WITH Docker
## General Docker Commands
* **docker-compose up** --> starts up all containers in project with terminal display
  * **docker-compose up -d** --> starts up all containers in project without terminal display (detached mode)
* **docker-compose down** --> shuts down all containers in project

* **docker exec -it cs-411w-orange-fall2023-django-1 bash** --> opens shell inside django server container
  * **python3 manage.py migrate** ---> Make sure db is up to date
  * **python3 manage.py createsuperuser** ---> Creates a superuser (admin)
  * **python3 manage.py loadMenuTags** ---> initializes the tag tables in database
  * **exit** --> exits django shell

* **docker compose build** --> Rebuilds django container (use when requirements.txt is updated)


## Load and Generate Commands (run in interactive shell)
* **python3 manage.py init** --> runs a series of default load commands that initializes the databse
  * This command calls the following commands:
  * **python3 manage.py loadMenuTags** --> loads the default menu tags
  * **python3 manage.py loadDefaultAccounts** --> loads the default patron, restaurant, and admin accounts
  * **python3 manage.py loadDefaultPatrons** --> loads the default patron profiles
  * **python3 manage.py loadDefaultRestaurants** --> loads the default restaurants

* **python3 manage.py generateRestaurants _int_** --> generates randomized restaurant information into restaurantBuffer.json
* **python3 manage.py loadRestaurants** --> loads restaurant json objects from restaurantBuffer.json (default) or a specified file (-f=_filepath_)
* **python3 manage.py generatePatrons _int_** --> generates randomized patron information into patronBuffer.json
* **python3 manage.py loadPatrons** --> loads patron json objects from patronBuffer.json (default) or a specified file (-f=_filepath_)


## For Backend Devs Only
* Use **docker-compose up** in dev branch
* Use **docker-compose -f docker-compose.yml up** in main branch (ignores override.yml)

Note:
* When running in main branch:
 * Use **docker-compose -f docker-compose.yml up**
 * This excludes the override file, defaulting to the main branch database
 * Make sure *settings.py* refers to 'secrets.json'
* When running in dev branch:
 * Use **docker-compose up**
 * This uses the override file to override the database used for development
 * Make sure *settings.py* refers to 'secrets_dev.json'

Note: See NOTES_DOCKER.md for more information




## Server pushes with Docker (Foster)
* **docker login -u wtfoster2**
* **docker tag __imageid__ wtfoster2/cs411wforang:__tag__**
* **docker push wtfoster2/cs411wforang:__tag__**
* **docker logout**




# WITHOUT Docker
## Virtual Environments
* **python3 -m venv .env** ---> Creates the - .env virtual environment
* **source .env/bin/activate** ---> Activates the virtual environment
* **deactivate** ---> Deactivates the virtual environment

## Common Commands
* **source .env/bin/activate** ---> Activates the virtual environment
* **python3 manage.py runserver** ---> Views the project in its current state
* **python3 manage.py migrate** ---> Make sure db is up to date
* **python3 manage.py createsuperuser** ---> Creates a superuser (admin)