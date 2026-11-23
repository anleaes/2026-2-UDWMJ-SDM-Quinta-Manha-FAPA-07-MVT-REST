from django.core.validators import MinValueValidator
from django.db import models

from pessoas.models import Pessoa


class Funcionario(Pessoa):
    """Equipe do escape room. Herda nome, e-mail, telefone... de Pessoa."""
    CARGO_CHOICES = [
        ('game_master', 'Game Master'),
        ('recepcionista', 'Recepcionista'),
        ('tecnico', 'Técnico de cenário'),
        ('gerente', 'Gerente'),
    ]

    cargo = models.CharField('Cargo', max_length=30, choices=CARGO_CHOICES, default='game_master')
    data_admissao = models.DateField('Data de admissão')
    salario = models.FloatField('Salário', default=0, validators=[MinValueValidator(0)])
    matricula = models.CharField('Matrícula', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'
