from django import forms
from horarios.models import Horario
from .models import Agendamento


class AgendamentoForm(forms.ModelForm):

    class Meta:
        model = Agendamento
        exclude = ()
        widgets = {
            'quantidade_pessoas': forms.NumberInput(attrs={'min': '0'}),
            'desconto': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só aparecem horários abertos para reserva (na edição, mantém o horário atual)
        abertos = Horario.objects.filter(status='disponivel')
        if self.instance.pk:
            abertos = abertos | Horario.objects.filter(pk=self.instance.horario_id)
        self.fields['horario'].queryset = abertos
