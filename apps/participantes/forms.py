from django import forms
from .models import Participante


class ParticipanteForm(forms.ModelForm):

    class Meta:
        model = Participante
        exclude = ()
        widgets = {
            'telefone': forms.TextInput(attrs={'data-mask': 'telefone', 'placeholder': '(11) 90000-0000'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }
