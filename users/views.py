from django.shortcuts import render, redirect
from .forms import ClienteForm

def register(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  

    else:
        form = ClienteForm()
    return render(request, 'users/register.html', {'form': form})
