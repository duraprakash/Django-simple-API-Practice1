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