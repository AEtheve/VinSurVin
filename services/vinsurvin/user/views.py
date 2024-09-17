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
            
            user = User.objects.create_user(username=username, email=email, password=password)

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
        data = json.loads(request.body)
        product_id = data.get('product')
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)

        user = request.user

        if not user:
            return JsonResponse({'error': 'Username not found'}, status=400)
        
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
        data = json.loads(request.body)
        product_id = data.get('product')
        quantity = int(data.get('quantity', 1))

        if not all([quantity, product_id]):
            return JsonResponse({'error': 'Quantity and Product ID are required'}, status=400)

        user = request.user

        if not user:
            return JsonResponse({'error': 'Username not found'}, status=400)

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
        username = request.user

        if not username:
            return JsonResponse({'error': 'Username not found'}, status=400)
        
        return JsonResponse({'cart': username.get_cart()}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
@require_http_methods(["GET"])
def get_user_info(request):
    try:
        username = request.user

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        return JsonResponse(username.get_info(), status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        user = request.user
        street = data.get('street')
        city = data.get('city')

        if not all([street, city]):
            return JsonResponse({'error': 'Address is required'}, status=400)

        order = user.create_order(street, city)
        return JsonResponse({'message': 'Order created successfully', 'order': order}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_orders(request):
    try:
        username = request.user

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        return JsonResponse({'orders': username.get_orders()}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def mark_order_delivered(request):
    try:
        data = json.loads(request.body)
        username = request.user
        order_id = data.get('order_id')

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        
        if not all([order_id]):
            return JsonResponse({'error': 'Order ID are required'}, status=400)
        
        if username.update_order_status(order_id, 'delivered'):
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
        data = json.loads(request.body)
        username = request.user
        order_id = data.get('order_id')

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        
        if not all([order_id]):
            return JsonResponse({'error': 'Username and order ID are required'}, status=400)

        if username.update_order_status(order_id, 'canceled'):
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
        user = request.user
        
        user.delete_cart()
        return JsonResponse({'message': 'Cart emptied successfully and stock updated'}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'One or more products in the cart no longer exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)