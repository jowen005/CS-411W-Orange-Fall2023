# WITH Docker
# General Docker Commands
* **docker-compose up** --> starts up all containers in project with terminal display
  * **docker-compose up -d** --> starts up all containers in project without terminal display (detached mode)
* **docker-compose down** --> shuts down all containers in project

* **docker exec -it cs-411w-orange-fall2023-django-1 bash** --> opens shell inside django server container
  * **python3 manage.py migrate** ---> Make sure db is up to date
  * **python3 manage.py createsuperuser** ---> Creates a superuser (admin)
  * **exit** --> exits django shell

# For Backend Devs Only
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