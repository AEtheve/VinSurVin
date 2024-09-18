from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from .models import User
from product.models import Product
from django.contrib.auth.models import AnonymousUser
import uuid
User = get_user_model()

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not all([username, email, password]):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            user = User.objects.create_user(username=username, email=email, password=password, is_anonymous_user=False)

            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not all([username, password]):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'message': 'Login successful', 'user': user.username}, status=200)

            return JsonResponse({'error': 'Incorrect username or password'}, status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        user = check_user_login(request)
        data = json.loads(request.body)
        product_id = data.get('product')
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)

        if user.add_to_cart(product_id, quantity):
            return JsonResponse({'message': 'Product added to cart successfully', 'cart': user.get_cart()}, status=200)
        else:
            return JsonResponse({'error': 'Insufficient stock'}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request):
    try:
        user = check_user_login(request)
        data = json.loads(request.body)
        product_id = data.get('product')
        quantity = int(data.get('quantity', 1))

        if not all([quantity, product_id]):
            return JsonResponse({'error': 'Quantity and Product ID are required'}, status=400)

        if user.remove_from_cart(product_id, quantity):
            return JsonResponse({'message': 'Product removed from cart successfully', 'cart': user.cart}, status=200)
        else:
            return JsonResponse({'error': 'Product not found in cart'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_cart(request):
    try:
        user = check_user_login(request)
        return JsonResponse({'cart': user.get_cart()}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
@require_http_methods(["GET"])
def get_user_info(request):
    try:
        user = check_user_login(request)
        return JsonResponse(user.get_info(), status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        user = check_user_login(request)
        data = json.loads(request.body)
        street = data.get('street')
        city = data.get('city')
        zip_code = data.get('zip_code')
        if not all([street, city, zip_code]):
            return JsonResponse({'error': 'Address is required'}, status=400)
        
        email = None
        if user.is_anonymous_user:
            email = data.get('email')
            if not email:
                return JsonResponse({'error': 'Email is required for anonymous users'}, status=400)

        order = user.create_order(street, city, zip_code, email=email)
        return JsonResponse({'message': 'Order created successfully', 'order': order}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_orders(request):
    try:
        user = check_user_login(request)
        return JsonResponse({'orders': user.get_orders()}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def mark_order_delivered(request):
    try:
        user = check_user_login(request)
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        if not all([order_id]):
            return JsonResponse({'error': 'Order ID are required'}, status=400)
        
        if user.update_order_status(order_id, 'delivered'):
            return JsonResponse({'message': 'Order marked as delivered'}, status=200)
        else:
            return JsonResponse({'error': 'Order not found'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def cancel_order(request):
    try:
        user = check_user_login(request)
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        if not all([order_id]):
            return JsonResponse({'error': 'Order ID is required'}, status=400)

        if user.update_order_status(order_id, 'canceled'):
            return JsonResponse({'message': 'Order canceled'}, status=200)
        else:
            return JsonResponse({'error': 'Order not found'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_cart(request):
    try:
        user = check_user_login(request)
        
        user.delete_cart()
        return JsonResponse({'message': 'Cart emptied successfully and stock updated'}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'One or more products in the cart no longer exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)    

def check_user_login(request):
    if isinstance(request.user, AnonymousUser):
        username = str(uuid.uuid4())
        user = User.objects.create_user(username=username, is_anonymous_user=True)
        auth_login(request, user)
        return user
    return request.user

def is_user_logged(request):
    return not isinstance(request.user, AnonymousUser)
