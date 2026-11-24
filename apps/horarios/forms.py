from django import forms
from .models import Horario


class HorarioForm(forms.ModelForm):

    class Meta:
        model = Horario
        exclude = ()
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'vagas_disponiveis': forms.NumberInput(attrs={'min': '0'}),
        }
