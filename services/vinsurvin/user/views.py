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
                return JsonResponse({'error': 'Tous les champs sont requis'})
            
            user = User.objects.create_user(username=username, email=email, password=password)

            return JsonResponse({'message': 'Utilisateur créé avec succès'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not all([username, password]):
                return JsonResponse({'error': 'Tous les champs sont requis'})
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'message': 'Connexion réussie', 'user': user.username})

            return JsonResponse({'error': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product')
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({'error': 'Product ID est requis'}, status=400)

        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'error': 'Utilisateur non authentifié'}, status=401)

        print(user, product_id, quantity)
        
        if user.add_to_cart(product_id, quantity):
            return JsonResponse({'message': 'Produit ajouté au panier avec succès', 'cart': user.get_cart()})
        else:
            return JsonResponse({'error': 'Stock insuffisant'}, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        product_id = data.get('product')
        quantity = int(data.get('quantity', 1))

        if not all([username, product_id]):
            return JsonResponse({'error': 'Username et Product ID sont requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

        if user.remove_from_cart(product_id, quantity):
            return JsonResponse({'message': 'Produit retiré du panier avec succès', 'cart': user.cart})
        else:
            return JsonResponse({'error': 'Produit non trouvé dans le panier'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_cart(request):
    try:
        username = request.user

        if not username:
            return JsonResponse({'error': 'Username est requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        return JsonResponse({'cart': user.get_cart()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
@require_http_methods(["GET"])
def get_user_info(request):
    try:
        username = request.user

        if not username:
            return JsonResponse({'error': 'Username est requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

        return JsonResponse(user.get_info())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')

        if not username:
            return JsonResponse({'error': 'Username est requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

        order = user.create_order()
        return JsonResponse({'message': 'Commande créée avec succès', 'order': order})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_orders(request):
    try:
        username = request.GET.get('username')

        if not username:
            return JsonResponse({'error': 'Username est requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

        return JsonResponse({'orders': user.get_orders()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def mark_order_delivered(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        order_id = data.get('order_id')

        if not all([username, order_id]):
            return JsonResponse({'error': 'Username and order ID are required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if user.update_order_status(order_id, 'delivered'):
            return JsonResponse({'message': 'Order marked as delivered'})
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
        username = data.get('username')
        order_id = data.get('order_id')

        if not all([username, order_id]):
            return JsonResponse({'error': 'Username and order ID are required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if user.update_order_status(order_id, 'canceled'):
            return JsonResponse({'message': 'Order canceled'})
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
        data = json.loads(request.body)
        username = data.get('username')

        if not username:
            return JsonResponse({'error': 'Username est requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

        user.delete_cart()
        return JsonResponse({'message': 'Panier vidé avec succès'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)