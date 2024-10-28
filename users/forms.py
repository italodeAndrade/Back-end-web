from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha')  # Campo adicional para entrada de senha

    class Meta:
        model = Cliente
        fields = ['email', 'nome']  # Remova 'senha' aqui

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['senha'])  # Define a senha criptografada
        if commit:
            cliente.save()
        return cliente
