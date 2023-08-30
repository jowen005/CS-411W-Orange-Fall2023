# Django Notes
## Virtual Environments
* **python3 -m venv .env** ---> Creates the - ll_env virtual environment
* **source .env/bin/activate** ---> Activates the virtual environment
  * packages installed in ll_env when environment is inactive will not be available
* **deactivate** ---> Deactivates the virtual environment

## Starting the Project
* **pip install django** ---> installs django
* **django-admin startproject project_name .** ---> sets up new project named ll_project, creating the following:
  * *manage.py*: a short program that takes commands and feeds them to the relevant part Django
  * *project_name*:
    * *settings.py*: controls how Django interacts with your system and manages the project
    * *urls.py*: tells Django which pages to build in response to browser requests
    * *wsgi.py*: helps Django serve the files it creates (web server gateway interface)

## Database
* **python3 manage.py migrate** ---> When running the first time, it creates a new database named db.sqlite3
* For MySQL configure *settings.py* and change the default database
* **pip install ______** ---> one of the following
  * **mysqlclient** ---> XXX cannot seem to get this to work XXX MUCH FASTER THOUGH
    * 'ENGINE' is 'django.db.backends.mysql'
  * **pymysql** ---> purely pythonic but not as fast as mysqlclient
    * 'ENGINE' is 'django.db.backends.mysql'
    * in *project/__init__.py* add the following lines
      * *import pymysql*
      * *pymysql.install_as_MySQLdb()*
  * **mysql-connector-python** ---> slowest of the 3
    * 'ENGINE' is 'mysql.connector.django'

## Viewing the Project
* **python3 manage.py runserver** ---> Views the project in its current state
  * This starts a <u>development server</u> so you can view your project on your system to see how well it works
  * Visit using the url **localhost:8000**

## Starting the App
* **python3 manage.py startapp app_name** ---> Tells Django to create the infrastructure needed to build an app
  * *app_name*:
    * *models.py*: defines the data we want to manage in our app
    * *admin.py*: registers models to manage
    * *views.py*: renders a template into a view
  * Open a new terminal window to execute this command as the server needs to continue running

## Models
* Models are used to define the data we want to manage
  * Define this data in the form of a class in the *models.py* file
  * To activate the models you **MUST** add your app to the INSTALLED_APPS list in *settings.py*
  * Next, execute **python3 manage.py makemigrations app_name**:
    * **makemigrations** tells Django to figure out how to modify the database so it can store the data associated with any new models we've defined. This creates a *migration* file.
  * Then, execute **python3 manage.py migrate** to modify the database by applying the migration

Whenever we want to modify the data that the *app_name* manages we:
1. modify *models.py*
2. call *makemigrations* on *app_name*
3. tell Django to *migrate* the project

## Admin
* Django's *admin site* is only meant to be used by the site's administrators
* Creating a Super User:
  * **python3 manage.py createsuperuser** ---> Creates a super user
* Add models to site manually in *admin.py*

## Moving the Project Directory
* **pip freeze > requirements.txt** ---> freeze yo requirements
* **deactivate** and **rm -rf .env** ---> deactivate and remove virtual environment
* Move the desired directory
* **python3 -m venv .env** and **source .env/bin/activate** ---> create a fresh venv and activate it
* **pip install -r requirements.txt** ---> Install all dependencies

## Django Shell Example with Topic Model
* This is an environment for testing and troubleshooting your project
* **python3 manage.py shell** ---> launches a python interpreter that you can use to explore the data stored in your project's database
  * Then **from app_name.models import Topic** to import the model Topic from the *learning_logs.models* module
  * and then **Topic.objects.all()** to the get all the instances of the model *Topic*

## Making Pages
* Making web pages with Django consists of 3 stages: 
  1. defining URLs
      * *URL pattern*: describes the way the URL is laid out
      * It also tells Django what to look for when matching a browser request with a site URL, so it knows which page to return
      * Each URL then maps to a view
  2. writing views
      * The *view* function retrieves and processes the data needed for that page
  3. writing templates
      * A view often renders the page using a *template*, which contains the overall structure of the page

## GET and POST Requests
* The two main tupes of requests are GET and POST
  * GET: Use GET requests for pages that only read data from the server
  * POST: Use POST requests when the user needs to submit information through a form
* When a user initially requests a page, their browser sends a GET request
* Once the user filles out and submits the form, their browser will submit a POST request
    * Depending on the request, we'll know whether the user is requesting a blank form (GET) or asking us to process a completed form (POST)
  
## Creating A Form
Basic steps is:
1. Create method in *forms.py*
2. Update *urls.py*
3. Create method in *views.py*
4. Create template in *templates/app_name/*
5. Make the new HTML page reachable from another template

## Styling
* django-bootstrap5 app: downloads required files, placing them in the appropriate locations, and making styling directives available in the project's templates
  * **pip install django-bootstrap5**

## Correct Order of initializing a Django Project with pymysql
Making an PyMySQL powered Django app for backend only (Have Python, MySQL, and MySQL Workbench installed)
1. Create virtual environment
   1. *python3 -m venv .env*
   2. *source .env/bin/activate*
2. Create database on MySQL server
   1. *mysql -u root -p*
   2. *CREATE DATABASE IF NOT EXISTS db;*
3. Install django and pymysql
   1. *pip install django pymysql*
4. Create project
   1. *django-admin startproject project_name .*
   2. edit database config in settings.py:
      'default': {
        #MySQL engine. Powered by the mysqlclient module
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lcc',
        'USER': 'root',
        'PASSWORD': '_____',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
   3. install as pymysql as mysqldb in __init__.py:
      import pymysql
      pymysql.install_as_MySQLdb()
5. Migrate initial django stuff
   1. *python3 manage.py migrate*
   2. Check to make sure it uploaded to mysql server
6. Create app and models
   1. *python3 manage.py startapp app_name*
   2. dont forget *class Meta: db_table=""* in model for naming it
7. Migrate models and check on mysql server
   1. *python3 manage.py makemigrations app_name*
   2. *python3 manage.py migrate*
8. Setup super user and double check on admin site (dont forget to register models)
   1. *python3 manage.py createsuperuser*
   
## Setting up APIs
We will use *djangorestframework* and *django-cors-headers*
* Use **pip install** to install these in the virtual environment
  * *django-cors-headers*
    * Prevents errors that you normally get due to CORS rules
    * Whitelist *localhost:3000* so the frontend can be served on that port and interact with the API
  * *djangorestframework*

Create Serializers
* Serializers convert model instances to JSON so that the frontend can work with the received data
* Create a file *serializers.py* in the same folder as *models.py*
* Create a Serializer for every model you want serialized using *serializers.ModelSerializer*

Create View
* Import model and serializer into *views.py*
* Create a model view using *viewsets.ModelViewSet* from *rest_framework*

Set the API URLs in *project_name/urls.py*
* Declare a router
* Register the serializer viewset with the router

# Deploying
## Setting up Platform.sh
In this activity we use *platform.sh*
* Use this command to install platform.sh CLI
  * curl -fsSL https://raw.githubusercontent.com/platformsh/cli/main/installer.sh | bash
* In active virtual environment, issue this command to install this package that helps detect whether the project is running on your local system on platform.sh
  * *pip install platformshconfig*
* Create a requirements.txt file to list which packages Learning Log depends on
  * *pip freeze > requirements.txt*
* Add the following package in a *requirements_remote.txt* file in the same directory as *requirements.txt*
  * gunicorn
    * Responds to requests as they come in to the remote server
  * psycopg2
    * Required to let Django manage the Postgres database that Platform.sh uses

## Adding Config Files
* .platform.app.yaml
  * controls the overall deployment process
  * *relationships:* describes other services the project needs
  * *commands:start:* tells Platform.sh what process to use to serve incoming requests
  * *locations* tells Platform.sh where to send incoming requests
  * *mounts* lets us define directories where we can read and write data
  * *hooks* defines actions that are taken at various points during the deployment process
    * In the *build* section we install all the packages that are required to serve the project in the live environment
    * *collectstatic* is used to collect all the static files needed for the project into one place so they can be served efficiently
  * *deploy* is used to specify that migrations should be run each time the project is deployed
* .platform/routes/yaml
  * makes sure requests like https://project_url.com and www.project_url.com all get routed to the same place
* .platform/services.yaml
  * specifies services that our project needs in order to run

## Using Git to Track the Project's Files
Set up personal information
* *git config --global user.name "eric"*
* *git config --global user.email "eric@example.com"*

Commit the Project
* *git init*
* *git add .*
* *git commit -am "..."*
* *git status*

Creating a Project on Platform.sh
* *platform login* followed by *Y* to opebn a browser tab to log in
* *platform create* creates a project (input the name, region, plan, environment number, and storage)
* *platform push* pushes the project to platform.sh
* *platform url* returns the the urls for the project

## Refining Platform.sh deployment
Create a Superuser on Platform.sh
* Start a SSH session to run management commands on remote server (all existing users exist only on local server)
  * *platform environment:ssh*
* Create a superuser
  * *python manage.py createsuperuser*

## Securing the Live Project
* Set DEBUG to False in *settings.py*

## Deleting a Project on Platform.sh
* *platform project:delete*
* Remove the remote from the command line by
  * *git remote*
  * *git remote remove platform*


