Note:: Upcoming steps will be given in instructions.txt of this repository

1. create virtual environment
py -m venv venv

2. install django
pip install django

3. create django project
django-admin startproject config .

4. run server
py manage.py runserver

5. create django app
django-admin startapp todo

6. register app in settings.py 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
]

7. migrations
py manage.py makemigrations
py manage.py migrate
now, localhost:8000/admin can be seen

8. create superuser
py manage.py createsuperuser
username: admin
email address: duraprakash141@gmail.com
password: aa11aa22
password again: aa11aa22
now, localhost:8000/admin can be login using these username and password

9. create model class
    from django.db import models

    # Create your models here.
    class Todo(models.Model):
        title = models.CharField(max_length=250, null=False, blank=False)
        description = models.CharField(max_length=250, null=False, blank=False)
        is_completed = models.BooleanField(default=False)
        created_at  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

10. register model in admin.py
    from django.contrib import admin
    from .models import Todo

    # Register your models here.
    admin.site.register(Todo)

    now, http://localhost:8000/admin/ after login, todo model can be seen in the admin panel
    howeve, inserting or creating record from admin panel will fails.

11. migrations to fix inserting/creating records in admin panel
py manage.py makemigrations
py manage.py migrate
now, CRUD is possible in admin panel

============= Todo app ===========
============= CRUD start ===========
12. add functions in todo/views.py
   from django.shortcuts import render
from django.http import JsonResponse
from .models import Todo
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

    # list all todos
    def list_todo(request):
        try:
            todos = Todo.objects.all() # ORM quetyset to get all todo list
            todo = [] # new empty todo list
            for i in todos: # loop through todos
                todo.append( # append every item of todos into todo
                    { # transforming data into json format
                        'id': i.pk,
                        'title': i.title,
                        'description': i.description,
                        'is_completed': i.is_completed,
                    }
                )
            return JsonResponse(todo, safe=False)
        except Todo.DoesNotExist:
            return JsonResponse({'message':'Todo Not Found'}, safe=False)

    # retrieve todo by id
    def retrieve_todo(request, todoId):
        try:
            todo = Todo.objects.get(id=todoId) # ORM queryset to get todo list of id
            return JsonResponse(
                    { # transforming data into json format
                        'id': todo.pk,
                        'title': todo.title,
                        'description': todo.description,
                        'is_completed': todo.is_completed,
                    },
                    safe=False
                )
        except Todo.DoesNotExist:
            return JsonResponse({'message':'Todo Not Found'}, safe=False)

    # update todo by id
    def update_todo(request, todoId):
        try:
            todo = Todo.objects.get(id=todoId) # ORM queryset to get todo list of id

            todo.is_completed = not todo.is_completed # change completed status
            
            todo.save() # save the changes
            # return JsonResponse({'message':'Todo Updated Successfully'}, safe=False)
            return JsonResponse(
                    { # transforming data into json format
                        'id': todo.pk,
                        'title': todo.title,
                        'description': todo.description,
                        'is_completed': todo.is_completed,
                    },
                    safe=False
                )
        except Todo.DoesNotExist:
            return JsonResponse({'message':'Todo Not Found'}, safe=False)

    # delete todo by id
    def delete_todo(request, todoId):
        try:
            todo = Todo.objects.get(id=todoId) # ORM queryset to get todo list of id

            # todo.delete() # delete
            return JsonResponse({'message':'Todo Deleted Successfully'}, safe=False)
        except Todo.DoesNotExist:
            return JsonResponse({'message':'Todo Not Found'}, safe=False)

    # create todo
    @csrf_exempt
    def create_todo(request):
        if request.method == 'POST':
            # Check if request is JSON or form data
            try:
                data = json.loads(request.body)
                title = data.get("title")
                description = data.get("description", "")
                is_completed = data.get("is_completed", False)
            except json.JSONDecodeError:
                title = request.POST.get("title")
                description = request.POST.get("description", "")
                is_completed = request.POST.get("is_completed", False)

            # Create new todo
            new_todo = Todo.objects.create(
                title=title,
                description=description,
                is_completed=is_completed
            )
            return JsonResponse({'message': 'Todo Created'}, status=201)
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)

    Note:: creating/inserting of data in the todo is done 
        but doesn't support params, use postman to test,
        moreover, csrf or token is directly given inside function,
        so, token is not required while testing with post man.
            
            testing in postman: 
            method 1: select body, raw and JSON
            post -> http://localhost:8000/todos/create/
                    {
                        "title": "Buy a sharpner",
                        "description": "A sharpner to sharpen the pencil",
                        "is_completed": false
                    }

            method 2: select form-data, and fill the keys with values
            post -> http://localhost:8000/todos/create/
                    title - Buy a sharpner
                    description - A sharpner to sharpen the pencil
                    is_completed - false

            ======== DOES NOT SUPPORT======
            method 3: select params, and fill the keys with values
            post -> http://localhost:8000/todos/create/
                    title - Buy a sharpner
                    description - A sharpner to sharpen the pencil
                    is_completed - false
            ======== DOES NOT SUPPORT======

13. add urls.py in todo/urls.py
    from django.urls import path
    from .views import list_todo

    urlpatterns = [
        path('', list_todo),
    ]

14. changes in config/urls.py
    from django.urls import path
    from .views import list_todo, retrieve_todo, update_todo, delete_todo

    urlpatterns = [
        path('', list_todo),
        path('<int:todoId>/', retrieve_todo),
        path('<int:todoId>/update/', update_todo),
        path('<int:todoId>/delete/', delete_todo),
    ]
============= CRUD end ===========
