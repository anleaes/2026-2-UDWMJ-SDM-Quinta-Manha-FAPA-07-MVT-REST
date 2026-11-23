from django.db import models

from pessoas.models import Pessoa


class Cliente(Pessoa):
    """Quem faz a reserva. Herda nome, e-mail, telefone... de Pessoa."""
    cpf = models.CharField('CPF', max_length=14, unique=True)
    cidade = models.CharField('Cidade', max_length=80)
    data_cadastro = models.DateField('Data de cadastro', auto_now_add=True)
    observacoes = models.TextField('Observações', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'
