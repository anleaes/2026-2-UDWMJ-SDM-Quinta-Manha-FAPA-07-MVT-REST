from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models

from jogos.models import Jogo


class Horario(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('lotado', 'Lotado'),
        ('bloqueado', 'Bloqueado'),
        ('encerrado', 'Encerrado'),
    ]

    data = models.DateField('Data')
    hora_inicio = models.TimeField('Início')
    hora_fim = models.TimeField('Fim', null=True, blank=True,
                                help_text='Deixe em branco para calcular pela duração da sala.')
    vagas_disponiveis = models.PositiveIntegerField('Vagas', null=True, blank=True,
                                                    help_text='Deixe em branco para usar a capacidade máxima da sala.')
    status = models.CharField('Situação', max_length=15, choices=STATUS_CHOICES, default='disponivel')
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='horarios', verbose_name='Jogo')

    class Meta:
        verbose_name = 'Horário'
        verbose_name_plural = 'Horários'
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f'{self.jogo.nome} - {self.data:%d/%m/%Y} {self.hora_inicio:%H:%M}'

    def _fim_calculado(self):
        """Hora de fim informada, ou início + duração da sala."""
        if self.hora_fim:
            return self.hora_fim
        if self.hora_inicio and self.jogo_id:
            inicio = datetime.combine(self.data or datetime.today().date(), self.hora_inicio)
            return (inicio + timedelta(minutes=self.jogo.sala.duracao_minutos)).time()
        return None

    def clean(self):
        fim = self._fim_calculado()
        if self.hora_inicio and self.hora_fim and self.hora_fim <= self.hora_inicio:
            raise ValidationError('A hora de fim precisa ser depois da hora de início.')
        # Regra: a mesma sala não pode ter dois horários sobrepostos no mesmo dia
        if self.jogo_id and self.data and self.hora_inicio and fim and fim > self.hora_inicio:
            conflito = (Horario.objects
                        .filter(jogo__sala=self.jogo.sala, data=self.data,
                                hora_inicio__lt=fim, hora_fim__gt=self.hora_inicio)
                        .exclude(pk=self.pk)
                        .exists())
            if conflito:
                raise ValidationError(f'A sala "{self.jogo.sala.nome}" já tem um horário que se sobrepõe a este.')

    def save(self, *args, **kwargs):
        if self.jogo_id:
            if self.hora_fim is None:
                self.hora_fim = self._fim_calculado()
            if self.vagas_disponiveis is None:
                self.vagas_disponiveis = self.jogo.sala.capacidade_maxima
        # Regra: sem vagas = lotado; com vagas = disponível (bloqueado/encerrado ficam como estão)
        if self.status in ('disponivel', 'lotado'):
            self.status = 'lotado' if (self.vagas_disponiveis or 0) <= 0 else 'disponivel'
        super().save(*args, **kwargs)
