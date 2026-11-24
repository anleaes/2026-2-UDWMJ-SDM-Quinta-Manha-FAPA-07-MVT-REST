from datetime import date

from django.db import models

from pessoas.models import Pessoa


class Participante(Pessoa):
    """Quem entra na sala para jogar. Herda nome, e-mail, telefone... de Pessoa."""
    documento = models.CharField('Documento (RG/CPF)', max_length=20, blank=True)
    menor_de_idade = models.BooleanField(
        'Menor de idade', default=False,
        help_text='Se a data de nascimento for preenchida, este campo é calculado sozinho.')
    termo_responsabilidade = models.FileField(
        'Termo de responsabilidade', upload_to='termos', blank=True,
        help_text='Obrigatório para menores de idade (PDF ou foto).')
    observacoes = models.TextField('Observações', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'

    def save(self, *args, **kwargs):
        # Regra: com a data de nascimento, o sistema descobre sozinho se é menor
        if self.data_nascimento:
            hoje = date.today()
            nasc = self.data_nascimento
            idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            self.menor_de_idade = idade < 18
        super().save(*args, **kwargs)
