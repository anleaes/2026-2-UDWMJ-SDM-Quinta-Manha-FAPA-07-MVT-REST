from django import forms
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        exclude = ()
        widgets = {
            'telefone': forms.TextInput(attrs={'data-mask': 'telefone', 'placeholder': '(11) 90000-0000'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'salario': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
