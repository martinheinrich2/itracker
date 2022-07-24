# Issue Tracker App

## Project steps using PyCharm, sets up virtual environment

1. Set up folder structure, e.g. like in the Book "Flask Web Development and also on GitHub [https://github.com/miguelgrinberg/flasky](https://github.com/miguelgrinberg/flasky).
2. Download and install PostgreSQL
3. Create virtual environment, e.g. use available requirements.txt
4. Create .env and .flaskenv files with environment variable definitions, install python-dotenv and use the from_prefixed_env() prefix to load environment varialbes.
5. Create and run script to create new database
6. Create config.py file, separate default, development, testing and production configuration
7. Generate and update requirements.txt
8. Create extension.py file to store all extensions, import them in dunder init.py
9. Create dunder init files app/__init__.py and app/main/__init__.py, where main/__init__.py contains the blueprint
10. Add app/static folder with css, img and js
11. Add using Bootstrap 5.1.3, bootstrap.min.css to static/css; copy bootstrap.min.js and jquery-3.6.0.min.js to static/js folder
12. Set up simple templates, base.html. index.html, navbar.html and run app
13. First milestone is a running app with navbar
14. Create errors pages in templates (403, 404, 500)
15. Set up Git repository
16. Create database models.py
17. Create user table from script
18. Create login, register and change password forms and functions
19. Create unit tests for user model
20. Add user roles to models
21. Create unit tests for role model
22. Add flask-moment and modify base.html to display correct date/time
23. Add edit user profile page
24. Add issues and comments to model, update database
25. Add issues form, view and html files
26. Add comments form, view and html files
27. Display comments in issue
28. Display issues in issues and user page, add pagination
29. Add Admin or Moderator can edit/close issue
30. Add Admin can list users and change user role, name
31. Add Admin can edit and delete comment
32. Add departments to model, modify admin edit user to assign department
33. Connect issues to department
34. Add list issues of same department as user
35. Add mor options to status: Open, In Progress, In Review, Resolved, Closed
36. Add priorities to issues
37. Add Admin can disable user account, except its own. Login fails for disabled accounts.


## How to prepare the database and run the app

1. Make necessary changes to the .env file (user, password, etc.)
2. Make sure you have PostgreSQL installed and the server is running. 
3. The "create_postgresql_db.py" script lets you display all available databases 
   and create the "issue_tracker" and "test_db" databases. 
4. It is important that the config.py file can read the environment variables.
5. Create database tables from shell:
   
    export FLASK_APP=itracker.py</br>
    (env)$ flask shell</br>
    from itracker import db </br>
    db.create_all()<br>
    exit()<br>

6. You can check if the new tables have been created. Use a GUI or the CLI tool 'psql':
   1. On a Mac if you are running the Postgres.app, open Terminal and type:
        - cd /Applications/Postgres.app/Contents/Versions/latest/bin/
        - ./psql -h localhost -U postgres -d issue_tracker
        - \d+   *prints all tables in the database with additional information*
        - \d+ roles or \d user *prints a description of the table with additional information, use 'q' to exit view*
        - \q *quits from postgres shell*

7. Add roles to database from shell:

    export FLASK_APP=itracker.py</br>
    (env)$ flask shell</br>
    Role.insert_roles()
    Role.query.all()
    exit()

8. Run issue_tracker.py or run app in terminal


# Additional Operations
## Run app in Terminal 
export FLASK_APP=itracker.py </br>
flask run</br>

## Enter app from Flask shell
export FLASK_APP=itracker.py </br>
(env)$ flask shell</br>

use: app.url_map to show rules

## Create database tables from shell
export FLASK_APP=itracker.py</br>
(env)$ flask shell</br>
from itracker import db</br>
db.create_all()</br>
exit()</br>

## Update database after changes to model.py
export FLASK_APP=itracker.py</br>
(env)$ flask db init</br>
(env)$ flask db migrate -m 'Some Comment'</br>
(env)$ flask db upgrade</br>

## Add Roles to development database
export FLASK_APP=itracker.py</br>
(env)$ flask shell</br>
Role.insert_roles()
Role.query.all()
exit()

## Run unit test
Make sure the PostgreSQL is running</br>
export FLASK_APP=itracker.py</br>
(env) $ flask test</br>

## Create hexadecimal secret token
import secrets <br/>
print(secrets.token_hex(32))

## Info
In models.py the User class has the object UserMixin. UserMixin provides default
implementations for the models that Flask-Login expects user objects to have. Such as
is_authenticated, is_active, is_anonymous, get_id().