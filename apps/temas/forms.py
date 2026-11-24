from django import forms
from .models import Tema


class TemaForm(forms.ModelForm):

    class Meta:
        model = Tema
        exclude = ()
        widgets = {
            'faixa_etaria_minima': forms.NumberInput(attrs={'min': '0'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
