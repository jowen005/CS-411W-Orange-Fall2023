## Setting up environment WITH Docker
* WIP

## Setting up environment without Docker
Install Python 3.9 or 3.10, MySQL Server, and MySQL Workbench
1. Setting up MySQL Server
   1. If having trouble installing, follow machine specific instructions for initial setup (you should have already set a root password)
   2. Run MySQL Workbench
   3. Click on localhost connection
   4. Verify Server is running (Administration Pane -> Management -> Server Status)
   5. Go to Schemas Pane, Right Click anywhere within, and select 'Create Schema'
   6. Name the schema 'lcc_main', click Apply, and click 'Apply' again
   7. Now you have created a database named 'lcc_main' on your local machine
2. Clone GitHub Repo onto local machine
3. Create and activate virtual environment (execute in VSCode terminal)
   1. *python3 -m venv .env*
   2. *source .env/bin/activate* --> Keep this environment activated
   3. *pip install -r requirements.txt* --> installs dependencies to .env
4. Create 'secrets.json' file
   1. Full template file is found in Discord #backend-resources
   2. Set the value of "db_name" to "lcc_main" (the database you created)
   3. Set the value of "db_password" to your root's password
   4. Note: You can create other users in your mysql server, if you want to avoid using the root user (and replace the "db_user" and "db_password" values)
5. Migrate/setup database using Django
   1. *python3 manage.py migrate*
   2. You should now be able to see the new tables created by Django in MySQL Workbench
6. Create a superuser
   1. *python3 manage.py createsuperuser*
7. To run the server and start using the APIs
   1. *python3 manage.py runserver*
   2. Make sure no errors occur
   3. If not you can access API using API Endpoints listed in API_DOC.md
   4. This server is running on localhost:8000