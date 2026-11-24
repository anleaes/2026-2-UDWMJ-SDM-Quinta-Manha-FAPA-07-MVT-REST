import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from agendamentos.models import Agendamento


class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
        ('estornado', 'Estornado'),
    ]
    METODO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de crédito'),
        ('cartao_debito', 'Cartão de débito'),
        ('dinheiro', 'Dinheiro'),
    ]

    valor = models.DecimalField('Valor (R$)', max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    metodo = models.CharField('Forma de pagamento', max_length=20, choices=METODO_CHOICES, default='pix')
    status = models.CharField('Situação', max_length=15, choices=STATUS_CHOICES, default='pendente')
    data_vencimento = models.DateField('Vencimento', default=timezone.localdate)
    realizado_em = models.DateTimeField('Pago em', null=True, blank=True)
    codigo_transacao = models.CharField('Código da transação', max_length=40, blank=True,
                                        help_text='Deixe em branco para o sistema gerar.')
    comprovante = models.FileField('Comprovante', upload_to='comprovantes', blank=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='pagamentos',
                                    verbose_name='Agendamento')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-id']

    def __str__(self):
        return f'{self.codigo_transacao} - R$ {self.valor}'

    def save(self, *args, **kwargs):
        if not self.codigo_transacao:
            self.codigo_transacao = 'TX-' + uuid.uuid4().hex[:10].upper()
        # Regra: ao marcar como pago, grava a data/hora do pagamento
        if self.status == 'pago' and not self.realizado_em:
            self.realizado_em = timezone.now()
        super().save(*args, **kwargs)
        # Regra: reserva totalmente paga deixa de ser "pendente" e vira "confirmado"
        ag = self.agendamento
        if ag.status == 'pendente' and ag.total_pago >= ag.valor_total:
            Agendamento.objects.filter(pk=ag.pk).update(status='confirmado')
