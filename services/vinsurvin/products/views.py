from django.http import JsonResponse
from .models import product_collection
from bson.json_util import dumps
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@require_http_methods(["GET"])
def get_products(request):
    try:
        products = list(product_collection.find())
        return JsonResponse(json.loads(dumps(products)), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def add_product(request):
    try:
        product_data = {}
        fields = ["price", "description", "image", "name", "stock", "type", "domain", "producer", "millesime"]
        
        for field in fields:
            value = request.GET.get(field)
            if value is not None and value != "":
                if field == "price" or field == "stock":
                    product_data[field] = int(value)
                else:
                    product_data[field] = value
        
        if not product_data:
            return JsonResponse({"error": "No valid data provided"}, status=400)
        
        product_collection.insert_one(product_data)
        return JsonResponse({"message": "Product added successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)