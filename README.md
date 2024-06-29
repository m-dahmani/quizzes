
You work on a site that allows users to share quizzes with their friends. Quizzes are stored in a Quiz Model, 
which is located in an application called quizzes.


#  python3 -m venv env

#  source env/bin/activate

#  pip install django

#  pip freeze > requirements.txt

#  django-admin startproject quiz

#  cd quiz/
# Configure Django to use a custom User model
#  python manage.py startapp authentication 
#  python manage.py startapp quizzes

# python manage.py makemigrations
# python manage.py migrate


# Envirements :

Links
* [https://github.com/m-dahmani/quizzes.git]
* 
* https://www.linkedin.com/in/mohamed-d-a74627a9/


### → git clone git@github.com:m-dahmani/quizzes.git

### → python3 -m venv env

### → source env/bin/activate

### → pip install -r requirements.txt 

### → python manage.py showmigrations

### → python manage.py migrate

### → python manage.py createsuperuser

* Username: admin
  Email address: 
  * Password (again):
     * Password must contain a number
     * Bypass password validation and create user anyway? [y/N]: y

#### Superuser created successfully.


#### → python manage.py runserver 0.0.0.0:8000




# Steps to Follow for Question 3 Quiz:
## Create a custom permission(deactivate_quiz)
## Create a custom migration to apply the change
## Assign this permission to the moderators group
## Restrict access to the deactivate_quiz view







