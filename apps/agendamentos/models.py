import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import F, Sum
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from clientes.models import Cliente
from grupos.models import Grupo
from horarios.models import Horario


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    # Campos gerados pelo sistema (editable=False: não aparecem no formulário)
    codigo = models.CharField('Código', max_length=20, unique=True, editable=False)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    valor_total = models.DecimalField('Valor total', max_digits=10, decimal_places=2, default=0, editable=False)
    codigo_confirmacao = models.CharField('Código de confirmação', max_length=10, editable=False)

    quantidade_pessoas = models.IntegerField('Quantidade de pessoas', default=2)
    desconto = models.FloatField('Desconto (%)', default=0,
                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField('Situação', max_length=15, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField('Observações', max_length=500, blank=True)

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Cliente')
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Horário')
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='agendamentos', verbose_name='Grupo (opcional)')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.codigo} - {self.cliente.nome}'

    # ---------- valores ----------
    @property
    def total_pago(self):
        return self.pagamentos.filter(status='pago').aggregate(s=Sum('valor'))['s'] or Decimal('0')

    @property
    def saldo(self):
        return self.valor_total - self.total_pago

    def calcular_valor_total(self):
        """valor por pessoa (sala + adicional do jogo) x pessoas, menos o desconto em %."""
        jogo = self.horario.jogo
        total = (jogo.sala.valor_base + jogo.valor_adicional) * self.quantidade_pessoas
        desconto = Decimal(str(self.desconto or 0))
        total = total * (Decimal('100') - desconto) / Decimal('100')
        return total.quantize(Decimal('0.01'))

    # ---------- regras ----------
    def clean(self):
        if self.grupo_id and self.cliente_id and self.grupo.cliente_id != self.cliente_id:
            raise ValidationError('O grupo escolhido pertence a outro cliente.')
        if not self.horario_id or not self.quantidade_pessoas:
            return
        sala = self.horario.jogo.sala
        if not (sala.capacidade_minima <= self.quantidade_pessoas <= sala.capacidade_maxima):
            raise ValidationError(
                f'A sala "{sala.nome}" comporta de {sala.capacidade_minima} a {sala.capacidade_maxima} pessoas.')
        if self.status == 'cancelado':
            return
        # vagas que ainda existem neste horário (somando as que esta própria reserva já ocupa)
        disponiveis = self.horario.vagas_disponiveis or 0
        if self.pk:
            antigo = Agendamento.objects.filter(pk=self.pk).first()
            if antigo and antigo.status != 'cancelado' and antigo.horario_id == self.horario_id:
                disponiveis += antigo.quantidade_pessoas
        elif self.horario.status in ('bloqueado', 'encerrado'):
            raise ValidationError('Este horário não está aberto para reservas.')
        if self.quantidade_pessoas > disponiveis:
            raise ValidationError(f'Este horário só tem {disponiveis} vaga(s) disponível(is).')

    def _mexer_nas_vagas(self, horario_id, quantidade):
        """Soma (ou subtrai, se negativo) vagas e deixa o Horario recalcular a própria situação."""
        Horario.objects.filter(pk=horario_id).update(vagas_disponiveis=F('vagas_disponiveis') + quantidade)
        Horario.objects.get(pk=horario_id).save()

    def save(self, *args, **kwargs):
        antigo = Agendamento.objects.filter(pk=self.pk).first() if self.pk else None
        if not self.codigo:
            self.codigo = 'AG-' + uuid.uuid4().hex[:8].upper()
        if not self.codigo_confirmacao:
            self.codigo_confirmacao = uuid.uuid4().hex[:6].upper()
        self.valor_total = self.calcular_valor_total()
        with transaction.atomic():
            super().save(*args, **kwargs)
            # devolve as vagas da reserva antiga e tira as da nova
            if antigo and antigo.status != 'cancelado':
                self._mexer_nas_vagas(antigo.horario_id, antigo.quantidade_pessoas)
            if self.status != 'cancelado':
                self._mexer_nas_vagas(self.horario_id, -self.quantidade_pessoas)


@receiver(pre_delete, sender=Agendamento)
def devolver_vagas_ao_excluir(sender, instance, **kwargs):
    """Ao excluir uma reserva (direto ou em cascata), as vagas voltam para o horário."""
    if instance.status != 'cancelado':
        Horario.objects.filter(pk=instance.horario_id).update(
            vagas_disponiveis=F('vagas_disponiveis') + instance.quantidade_pessoas)
        horario = Horario.objects.filter(pk=instance.horario_id).first()
        if horario:
            horario.save()  # recalcula "lotado/disponível"
