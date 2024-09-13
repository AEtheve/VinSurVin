from django.http import JsonResponse
from bson.json_util import dumps
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json
from django.core.serializers import serialize
from bson import ObjectId

@require_http_methods(["GET"])
def get_products(request):
    try:
        products = Product.objects.all()
        product_list = json.loads(serialize('json', products))
        return JsonResponse(product_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(["GET"])
def get_product_by_name(request):
    try:
        search_query = request.GET.get('name', '')
        products = Product.objects.filter(name__icontains=search_query)
        product_list = json.loads(serialize('json', products))
        return JsonResponse(product_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["GET"])
def get_product(request, numero):
    try:
        product = Product.objects.get(numero=numero)
        product_data = json.loads(serialize('json', [product]))[0]
        return JsonResponse(product_data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)