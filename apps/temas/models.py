from django.db import models


class Tema(models.Model):
    CLASSIFICACAO_CHOICES = [
        ('livre', 'Livre'),
        ('10', '10 anos'),
        ('12', '12 anos'),
        ('14', '14 anos'),
        ('16', '16 anos'),
        ('18', '18 anos'),
    ]

    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', max_length=500)
    faixa_etaria_minima = models.IntegerField('Idade mínima', default=0)
    classificacao = models.CharField('Classificação', max_length=10, choices=CLASSIFICACAO_CHOICES, default='livre')
    ambientacao = models.CharField('Ambientação', max_length=150, blank=True,
                                   help_text='Ex.: luz baixa, sons de fundo, névoa...')
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'
