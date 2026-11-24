import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from agendamentos.models import Agendamento
from funcionarios.models import Funcionario


class Sessao(models.Model):
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    RESULTADO_CHOICES = [
        ('pendente', 'Pendente'),
        ('escapou', 'Escapou'),
        ('nao_escapou', 'Não escapou'),
    ]

    codigo = models.CharField('Código', max_length=20, unique=True, editable=False)
    inicio_real = models.DateTimeField('Início real', null=True, blank=True)
    fim_real = models.DateTimeField('Fim real', null=True, blank=True)
    status = models.CharField('Situação', max_length=15, choices=STATUS_CHOICES, default='agendada')
    resultado = models.CharField('Resultado', max_length=15, choices=RESULTADO_CHOICES, default='pendente')
    observacoes = models.TextField('Observações', max_length=500, blank=True)
    pontuacao_final = models.IntegerField('Pontuação final', default=0, validators=[MinValueValidator(0)])
    # RELAÇÃO UM-PARA-UM: cada reserva gera no máximo UMA sessão (e cada sessão pertence a uma reserva)
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='sessao',
                                       verbose_name='Agendamento')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='sessoes',
                                    verbose_name='Game Master responsável')

    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'
        ordering = ['-id']

    def __str__(self):
        return f'{self.codigo} - {self.agendamento.horario.jogo.nome}'

    def clean(self):
        if self.inicio_real and self.fim_real and self.fim_real <= self.inicio_real:
            raise ValidationError('O fim real precisa ser depois do início real.')
        if self.agendamento_id and self.pontuacao_final:
            maxima = self.agendamento.horario.jogo.pontuacao_maxima
            if self.pontuacao_final > maxima:
                raise ValidationError(f'A pontuação máxima deste jogo é {maxima}.')

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = 'SS-' + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)
        # Regra: sessão concluída marca a reserva como concluída
        if self.status == 'concluida':
            Agendamento.objects.filter(pk=self.agendamento_id).update(status='concluido')
