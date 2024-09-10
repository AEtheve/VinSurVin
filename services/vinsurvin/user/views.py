from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

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