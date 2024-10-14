from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro concluído! Você pode fazer login agora.')

    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

