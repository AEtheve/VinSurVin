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
def search_product(request):
    try:
        filters = {}
        
        name = request.GET.get('name')
        if name:
            filters['name__icontains'] = name

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price:
            filters['price__range'] = (float(min_price), float(max_price))
        elif min_price:
            filters['price__gte'] = float(min_price)
        elif max_price:
            filters['price__lte'] = float(max_price)

        type = request.GET.get('type')
        if type:
            filters['type__iexact'] = type

        region = request.GET.get('region')
        if region:
            filters['region__iexact'] = region

        appellation = request.GET.get('appellation')
        if appellation:
            filters['appellation__iexact'] = appellation

        millesime = request.GET.get('millesime')
        if millesime:
            filters['millesime'] = int(millesime)

        grape_variety = request.GET.get('grape_variety')
        if grape_variety:
            filters['grape_variety__iexact'] = grape_variety

        products = Product.objects.filter(**filters)
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