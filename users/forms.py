from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['email', 'nome', 'senha']
        widgets = {
            'senha': forms.PasswordInput(), 
        }
