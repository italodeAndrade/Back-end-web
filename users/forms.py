from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha')  

    class Meta:
        model = Cliente
        fields = ['email', 'nome']  

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['senha']) 
        if commit:
            cliente.save()
        return cliente
