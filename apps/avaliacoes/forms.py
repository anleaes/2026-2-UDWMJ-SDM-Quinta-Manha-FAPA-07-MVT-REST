from django import forms
from sessoes.models import Sessao
from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao
        exclude = ()
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
            'resposta_empresa': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só se avalia uma sessão que já foi concluída
        concluidas = Sessao.objects.filter(status='concluida')
        if self.instance.pk:
            concluidas = concluidas | Sessao.objects.filter(pk=self.instance.sessao_id)
        self.fields['sessao'].queryset = concluidas
