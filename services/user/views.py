from django.shortcuts import render
from .models import user_collection
from django.http import JsonResponse
# Create your views here.

def index(request):
    return JsonResponse({"message": "Hello World"})

def add_user(request):
    records = {
        "name": "Thib Ernation",
        "password": "123456",
    }
    user_collection.insert_one(records)
    return JsonResponse({"message": "User created"})

def get_user(request):
    users = list(user_collection.find({}, {'_id': 0}))  
    return JsonResponse({"users": users}, safe=False)