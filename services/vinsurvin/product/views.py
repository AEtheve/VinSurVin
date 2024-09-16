from django.http import JsonResponse
from bson.json_util import dumps
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json
from django.core.serializers import serialize
from bson import ObjectId
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@require_http_methods(["GET"])
def get_products(request):
    try:
        page = request.GET.get('page', 1)
        products = Product.objects.all()
        paginator = Paginator(products, 12) 
        
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)
        
        product_list = json.loads(serialize('json', products_page))
        
        return JsonResponse({
            'products': product_list,
            'total_pages': paginator.num_pages,
            'current_page': products_page.number
        }, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(["GET"])
def search_product(request):
    try:
        page = request.GET.get('page', 1)
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
        paginator = Paginator(products, 12) 
        
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)
        
        product_list = json.loads(serialize('json', products_page))
        
        return JsonResponse({
            'products': product_list,
            'total_pages': paginator.num_pages,
            'current_page': products_page.number
        }, safe=False)
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