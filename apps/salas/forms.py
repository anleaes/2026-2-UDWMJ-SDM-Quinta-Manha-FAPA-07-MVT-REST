from django import forms
from .models import Sala


class SalaForm(forms.ModelForm):

    class Meta:
        model = Sala
        exclude = ()
        widgets = {
            'valor_base': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'capacidade_minima': forms.NumberInput(attrs={'min': '0'}),
            'capacidade_maxima': forms.NumberInput(attrs={'min': '0'}),
            'duracao_minutos': forms.NumberInput(attrs={'min': '0'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
