from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
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
            username = data.get('email')
            password = data.get('password')

            if not all([username, password]):
                return JsonResponse({'error': 'Tous les champs sont requis'})
            
            user = User.objects.get(username=username)

            if not user.check_password(password):
                return JsonResponse({'error': 'Mot de passe incorrect'}, status=400)

            user_data = {
                'date_joined': user.date_joined,
            }
            
            return JsonResponse({'message': 'Connexion réussie', 'user': user_data})
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
        username = data.get('username')
        product_id = data.get('product')  # Changed from 'product_id' to 'product'
        quantity = int(data.get('quantity', 1))  # Convert to int

        if not all([username, product_id]):
            return JsonResponse({'error': 'Username et Product ID sont requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        
        user.add_to_cart(product_id, quantity)
        return JsonResponse({'message': 'Produit ajouté au panier avec succès', 'cart': user.cart})
    
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
        username = request.GET.get('username')

        if not username:
            return JsonResponse({'error': 'Username est requis'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        return JsonResponse({'cart': user.get_cart()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)