from django.shortcuts import render, redirect
from .forms import ClienteForm
from django.contrib.auth import authenticate
from .models import Cliente
from django.contrib.auth.hashers import check_password
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('users:login')

    else:
        form = ClienteForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            cliente = Cliente.objects.get(email=email)
            if check_password(senha, cliente.senha):
                return redirect(reverse('filmes:lista_filmes'))
            else:
                return render(request, 'users/login.html', {'error': 'Senha incorreta'})
        
        except Cliente.DoesNotExist:

            return render(request, 'users/login.html', {'error': 'Email não encontrado'})
    
    return render(request, 'users/login.html')