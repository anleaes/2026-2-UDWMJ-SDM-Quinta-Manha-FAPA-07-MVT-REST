from django.db import models

from clientes.models import Cliente
from participantes.models import Participante


class Grupo(models.Model):
    TIPO_CHOICES = [
        ('amigos', 'Amigos'),
        ('familia', 'Família'),
        ('empresa', 'Empresa'),
        ('escola', 'Escola'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField('Nome do grupo', max_length=100)
    tipo_grupo = models.CharField('Tipo de grupo', max_length=15, choices=TIPO_CHOICES, default='amigos')
    tamanho_estimado = models.IntegerField('Tamanho estimado', default=4)
    observacoes = models.TextField('Observações', max_length=500, blank=True)
    data_criacao = models.DateField('Criado em', auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='grupos', verbose_name='Cliente responsável')
    # RELAÇÃO MUITOS-PARA-MUITOS: um grupo tem vários participantes e um participante pode estar em vários grupos
    participantes = models.ManyToManyField(Participante, blank=True, related_name='grupos', verbose_name='Participantes')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'
