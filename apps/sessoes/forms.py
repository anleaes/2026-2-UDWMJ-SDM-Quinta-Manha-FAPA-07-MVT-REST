from django import forms
from agendamentos.models import Agendamento
from .models import Sessao


class SessaoForm(forms.ModelForm):

    class Meta:
        model = Sessao
        exclude = ()
        widgets = {
            'inicio_real': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'fim_real': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'pontuacao_final': forms.NumberInput(attrs={'min': '0'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só aparecem reservas que ainda não têm sessão (e que não foram canceladas)
        livres = Agendamento.objects.exclude(status='cancelado').filter(sessao__isnull=True)
        if self.instance.pk:
            livres = livres | Agendamento.objects.filter(pk=self.instance.agendamento_id)
        self.fields['agendamento'].queryset = livres
