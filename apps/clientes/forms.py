from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        exclude = ()
        widgets = {
            'cpf': forms.TextInput(attrs={'data-mask': 'cpf', 'placeholder': '000.000.000-00', 'maxlength': '14'}),
            'telefone': forms.TextInput(attrs={'data-mask': 'telefone', 'placeholder': '(11) 90000-0000'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }
