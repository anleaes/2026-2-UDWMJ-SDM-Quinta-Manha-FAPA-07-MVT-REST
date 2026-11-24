from django import forms
from .models import Grupo


class GrupoForm(forms.ModelForm):

    class Meta:
        model = Grupo
        exclude = ()
        widgets = {
            'tamanho_estimado': forms.NumberInput(attrs={'min': '0'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
            'participantes': forms.CheckboxSelectMultiple(),
        }
