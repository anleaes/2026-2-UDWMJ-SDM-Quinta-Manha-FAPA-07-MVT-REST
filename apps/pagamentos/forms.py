from django import forms
from .models import Pagamento


class PagamentoForm(forms.ModelForm):

    class Meta:
        model = Pagamento
        exclude = ()
        widgets = {
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'realizado_em': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
