from django.http import JsonResponse
from bson.json_util import dumps
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from .models import Product
import json

@require_http_methods(["GET"])
def get_products(request):
    try:
        products = Product.objects.all()
        product_list = json.loads(serialize('json', products))
        return JsonResponse(product_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
