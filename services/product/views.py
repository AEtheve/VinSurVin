from django.shortcuts import render
from django.http import JsonResponse
from .models import product_collection
from bson import ObjectId

# Create your views here.

def add_product(request):
    products = [
        {
            "name": "Saint-Joseph",
            "price": 9.99,
        },
        {
            "name": "Chateau Lafleur",
            "price": 15.99,
        },
        {
            "name": "Chateau Margaux",
            "price": 23.49,
        }
    ]
    result = product_collection.insert_many(products)
    return JsonResponse({"message": "Products created", "ids": [str(id) for id in result.inserted_ids]})

def get_product(request):
    products = list(product_collection.find({}, {'_id': 0}))
    return JsonResponse({"products": products}, safe=False)

def get_product_by_id(request, product_id):
    try:
        all_products = list(product_collection.find())
        
        if 0 < product_id <= len(all_products):
            product = all_products[product_id - 1]
            product['_id'] = str(product['_id']) 
            return JsonResponse({"product": product})
        else:
            return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)