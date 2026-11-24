from django.core.exceptions import ValidationError
from django.db import models


class Sala(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', max_length=500)
    capacidade_minima = models.IntegerField('Capacidade mínima', default=2)
    capacidade_maxima = models.IntegerField('Capacidade máxima', default=6)
    duracao_minutos = models.IntegerField('Duração (minutos)', default=60)
    valor_base = models.DecimalField(
        'Valor por pessoa (R$)', max_digits=10, decimal_places=2, default=0,
        help_text='Preço de cada participante nesta sala.')
    imagem = models.ImageField('Imagem', upload_to='salas', blank=True)
    ativa = models.BooleanField('Ativa', default=True)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['id']

    def __str__(self):
        return f'{self.nome}'

    def clean(self):
        if self.capacidade_minima and self.capacidade_maxima and self.capacidade_minima > self.capacidade_maxima:
            raise ValidationError('A capacidade mínima não pode ser maior que a máxima.')
