from django import forms
from .models import Jogo


class JogoForm(forms.ModelForm):

    class Meta:
        model = Jogo
        exclude = ()
        widgets = {
            'tempo_limite_minutos': forms.NumberInput(attrs={'min': '0'}),
            'pontuacao_maxima': forms.NumberInput(attrs={'min': '0'}),
            'valor_adicional': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'historia': forms.Textarea(attrs={'rows': 4}),
            'instrucoes': forms.Textarea(attrs={'rows': 4}),
        }
