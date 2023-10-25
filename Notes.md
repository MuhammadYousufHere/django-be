First install the django package

run -> pip install django

`
Before that check for pip latest updates installations

python -m pip install --upgrade pip

`
then create a project

python -m django startproject <project name>
or
django-admin startproject <name>

---then we need a project standalone.

run -> python manage.py startapp <app_name>

then we have to link these both together.
go inside settings.py Look for INSTALLED_APPS variable and place the name of the app

--> START THE APP SERVER
python manage.py runserver
should be able to access port 8000

--------TEMPLATES------------------
create a dir 'template' inside the root of project

create html filles
inside the html file we use - jinja templating engine.
which allows to display dynamic data.

we create blocks (overrideable peice of content'

---------------MIGRATIONS-------------------------------------

data base modal migrations

python manage.py makemigrations
then
python manage.py migrate

--------------ADMIN-------------------------------------------------

create user for admin
python manage.py createsuperuser
