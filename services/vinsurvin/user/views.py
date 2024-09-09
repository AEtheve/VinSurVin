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