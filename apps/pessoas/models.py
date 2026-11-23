from django.db import models


class Pessoa(models.Model):
    """
    Classe-mãe (HERANÇA). Cliente, Funcionario e Participante herdam daqui:
    cada um ganha nome, e-mail, telefone etc. sem repetir os campos.
    No banco, cada classe vira uma tabela e a filha aponta para a mãe (herança multi-table).
    """
    nome = models.CharField('Nome', max_length=120)
    email = models.EmailField('E-mail', max_length=120, blank=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'

    @property
    def tipo(self):
        """Diz de que "filha" esta pessoa é (Cliente, Funcionário ou Participante)."""
        for atributo, rotulo in (
            ('cliente', 'Cliente'),
            ('funcionario', 'Funcionário'),
            ('participante', 'Participante'),
        ):
            if hasattr(self, atributo):
                return rotulo
        return 'Pessoa'
