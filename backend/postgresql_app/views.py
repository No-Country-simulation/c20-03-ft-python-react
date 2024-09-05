from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

@csrf_exempt
@require_POST
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_GET
def list_users(request):
    try:
        # Exclude superusers
        users = User.objects.filter(is_superuser=False).values('username', 'email')
        user_list = list(users)
        return JsonResponse({'users': user_list}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# New product upload view
@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')  # Asume que tienes una vista para listar productos
    else:
        form = ProductForm()
    return render(request, 'upload_product.html', {'form': form})