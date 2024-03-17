from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def list_todo(request):
    return JsonResponse({'message':'List todo'}, safe=False)

def retrieve_todo(request, todoId):
    return JsonResponse({'message':'Retrieve todo'}, safe=False)

def update_todo(request, todoId):
    return JsonResponse({'message':'Update todo'}, safe=False)

def delete_todo(request, todoId):
    return JsonResponse({'message':'Delete todo'}, safe=False)