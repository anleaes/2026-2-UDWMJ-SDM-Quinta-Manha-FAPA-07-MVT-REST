from django.db import models

from salas.models import Sala
from temas.models import Tema


class Jogo(models.Model):
    NIVEL_CHOICES = [
        (1, 'Muito fácil'),
        (2, 'Fácil'),
        (3, 'Médio'),
        (4, 'Difícil'),
        (5, 'Extremo'),
    ]

    nome = models.CharField('Nome', max_length=120)
    historia = models.TextField('História', max_length=1000)
    nivel_dificuldade = models.IntegerField('Dificuldade', choices=NIVEL_CHOICES, default=3)
    tempo_limite_minutos = models.IntegerField('Tempo limite (min)', default=60)
    pontuacao_maxima = models.IntegerField('Pontuação máxima', default=1000)
    instrucoes = models.TextField('Instruções', max_length=1000, blank=True)
    valor_adicional = models.DecimalField(
        'Adicional por pessoa (R$)', max_digits=10, decimal_places=2, default=0,
        help_text='Somado ao valor por pessoa da sala.')
    ativo = models.BooleanField('Ativo', default=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='jogos', verbose_name='Sala')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='jogos', verbose_name='Tema')

    class Meta:
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'

    @property
    def valor_por_pessoa(self):
        return self.sala.valor_base + self.valor_adicional
