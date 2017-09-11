# # #
# BEGIN
# # #

#Load VENV and make app file structure
#Load Django VENV
#navigate to virtualenv folder and load it
$ source djangoEnv/bin/activate #mac
$ call djangoEnv/scripts/activate #windows
#to deactivate virtualenv, use command: "deactivate"

# # #
# FILE STRUCTURE
# # #

# project folder
# apps folder
    # templates folder
    # urls.py (for app)
    # views.py
# project management folder
    # settings.py
    # urls.py (another one)

#in terminal:
$ django-admin startproject project_name #whatever project name you want
$ cd project_name
$ mkdir apps
$ cd apps
$ touch __init__.py
$ python ../manage.py startapp app1_name #whatever app name you want

$ cd app1_name
$ touch urls.py
$ mkdir templates
$ mkdir templates/app1_name
#and add any html files you want

#now open the main project file in your fave text editor

#in project folder: add app1_name in settings.py
'apps.app1_name', #remember the comma
#in project folder: in urls.py include urls
from django.conf.urls import url, include
url(r'^', include('apps.app1_name.urls')),

#in app folder: adding routes in urls.py
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
]
#in app folder: add an index method in views.py
def index(request):
    return render(request, 'app1_name/index.html')

$ python manage.py runserver #start server

#good libraries you'll probs want:
from django.shortcuts import render, redirect

# # #
# Model Layer
# # #

#good to plan this first

#plan the ERD by drawing it out in SQL Workbench or by hand on some paper.

#creating the ORM

#models.py
class User(models.Model):
    email = models.CharField(max_length = 38)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager() #connect model to UserManager
    #good if you want model level validations
    #if you don't need model level validations, you don't need this

    #this unicode code when you print an object in terminal will display it with given information (good for debugging)

    def __unicode__(self):
        return "id: " + str(self.id) + ", email: " + self.email

class Coment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name = "comments")#this creates foreign key & relationship between Comments & Users table

# RUN MIGRATIONS
#after writing out models, u must migrate them so that Django creates the SQL tables for you
python manage.py makemigrations
python manage.py migrate

#running shell:
$ python ./manage.py shell

# INTERACTING WITH ORM
#once shell is running, import table
from apps.[[app_name]].models import [[table_name]]

#views.py (referring to model thru ORM)
User.objects.create(email="email@email.com")
User.objects.all() #see all Users
u = User.objects.get(pk=id) #get a single user of given id
u.delete() #delete user

# MODEL LEVEL VALIDATIONS
#remember to use objects = UserManager() syntax

#models.py
class UserManager(models.Manager):
    def login(self, postData):
        #validation code here
        return [[stuff to return]]

#user.py
user_hash = {
    "email" : request.POST["email"]
}

#use this line to call the login method in UserManager
#pass it the argument user_hash as the parameter postData
user = User.objects.login(user_hash)

# CREATING INITIAL SEED DATA

$ python ./manage.py shell #open shell
from apps.app1_name.models import User #import User class

#now you can run ORM commands!
User.objects.create(email="first.last@email.com")
User.objects.all() #see all existing User objects

exit() #exit python shell

# # #
# views.py & urls.py
# # #

# CREATE METHODS AND ROUTES
#it's a good idea to create GET routes/methods before POST routes/methods
#check wireframe and decide on all routes/methods for each page
#for GET routes, render a template at the end of method

#urls.py
urlpatterns = [
    url(r'^$', views.index),
    url(r'^comment/process$', views.comment_process),
    url(r'^comment/success/(?P<id>\d+)$', views.comment_success), #regex for matching comment with comment id
]

#views.py
def index(request):
    return render(request, 'main_page/index.html')

# BUILD HTML
#flesh out your html

# ADD TEMPLATE PASS THRU DATA (if applicable)
#assign value in views.py and pass the value to html file as parameter of render:...*(scroll down to **DJANGO Template Language)

# ADD SESSION DISPLAY DATA (if applicable)
#if you must display session data, first set the data to a hardcoded number in your views.py method
#then display that session data in html file using django template language
#and make sure that works before adding more complex data...**(scroll down to **session below)

# CREATE POST ROUTES AND METHODS
#post routes handle submitted form data: creating, updating, deleting data
#usually you will redirect to another GET route after a post route is complete
#after you run all your POST route code, you are sending a response to the client
#telling it to make another request to another route (GET), where you'll render a template

#tip: build the route and associated method first

#check whether a request is a POST:
if request.method == "POST"

#reading form data:
request.POST['email']

#redirecting to GET route:
return redirect("/result")

# # #
# *DJANGO Template Language
# # #

#views.py
def result (request): 
    context = {
        "email": "email@email.com"
    }
    return render(request, 'survey_form/show.html', context)

#show.html
#context dictionary is passed into template with the render metnod
#now you can use the content of context in the show.html like so:
<p>Email: {{email}}</p>

#also, you can do some simple logic in the html, but don't overdo it! the main logic should be in the backend.

#for loop:
{% for u in userarray %}
    userID: {{userarray.0.id}}
    userEmail: {{u.0.email}}
{% endfor %}

#if statement:
{% if true %}
    #code here
{% endif %}

#**SESSION
#reading from session:
{{request.session.item}} #NOT {{request.session['item']}}

#reading from an array
{{myArray.0}} # NOT {{myArray[0]}}

# # #
# Sessions
# # #
#stored in dictionary format
#don't store too much in session! the logged-in user id or such is fine

#assigning data to a session:
request.session['user_id'] = 5
request.session['foods'] = [['apples', 5], ['pies', 1]]

#session data structure looks like this:
# session = {
#   'user_id' : 5
#   'foods' : [
#       ['apples', 5],
#       ['pies', 1]
#   ]
# }

#clearing session data:
request.session.clear()

#checking for empty session:
#before setting a value for a session key, the value defaults to 'None'
#if you try and get a value before it's been set, Python will throw you an error, so you have to use this syntax to check whether it exists or not:
if request.session.get('user_id') == None:

# # #
# Forms
# # #

<form action='/friends' method='post'>
    {% csrf_token %} #needed as security measure
    <label for="email">Email:<input type="text" name="email" id="email"></label>
</form>

#button
<input type="submit" value="update">

# # #
# Debugging
# # #    
#one method of debugging is using embed to add beakpoints to your code
$pip install ipython #in terminal with environment running
from IPython import embed #add this to top of .py file
embed() #will create a breakpoint

#you can also run the python shell so that you can build out your ORM layer
python ./manage.py shell
from apps.courses.models import User
User.objects.all()



