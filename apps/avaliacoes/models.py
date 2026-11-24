from django.db import models

from clientes.models import Cliente
from sessoes.models import Sessao


class Avaliacao(models.Model):
    NOTA_CHOICES = [
        (1, '1 - Péssimo'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente'),
    ]

    nota = models.IntegerField('Nota geral', choices=NOTA_CHOICES, default=5)
    nota_atendimento = models.IntegerField('Nota do atendimento', choices=NOTA_CHOICES, default=5)
    comentario = models.TextField('Comentário', max_length=500, blank=True)
    recomendaria = models.BooleanField('Recomendaria a amigos', default=True)
    criada_em = models.DateTimeField('Criada em', auto_now_add=True)
    resposta_empresa = models.TextField('Resposta da empresa', max_length=500, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name='Cliente')
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name='Sessão')

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-criada_em']
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'sessao'], name='uma_avaliacao_por_cliente_e_sessao'),
        ]

    def __str__(self):
        return f'{self.cliente.nome} - nota {self.nota}'
