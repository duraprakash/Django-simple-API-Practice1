from django.shortcuts import render
from django.http import JsonResponse
from .models import Todo

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
