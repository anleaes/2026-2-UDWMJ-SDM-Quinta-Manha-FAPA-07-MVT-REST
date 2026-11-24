"""
Comando: python manage.py popular_demo

Cria dados de DEMONSTRAÇÃO (salas, jogos, clientes, reservas...) e um usuário de teste,
para você ver o sistema "vivo" logo na primeira execução.
Só roda se TODOS os apps do projeto estiverem instalados (settings.py + urls.py).
"""
import io
import random
from datetime import date, datetime, timedelta

from django.apps import apps
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

APPS_NECESSARIOS = [
    ('pessoas', 'Pessoa'), ('clientes', 'Cliente'), ('funcionarios', 'Funcionario'),
    ('participantes', 'Participante'), ('salas', 'Sala'), ('temas', 'Tema'), ('jogos', 'Jogo'),
    ('horarios', 'Horario'), ('grupos', 'Grupo'), ('agendamentos', 'Agendamento'),
    ('pagamentos', 'Pagamento'), ('sessoes', 'Sessao'), ('avaliacoes', 'Avaliacao'),
]


def gerar_imagem(cor1, cor2):
    """Cria uma imagem 800x500 (degradê + um "buraco de fechadura") para ilustrar a sala."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None
    largura, altura = 800, 500
    img = Image.new('RGB', (largura, altura))
    draw = ImageDraw.Draw(img)
    for y in range(altura):
        t = y / altura
        cor = tuple(int(cor1[i] * (1 - t) + cor2[i] * t) for i in range(3))
        draw.line([(0, y), (largura, y)], fill=cor)
    cx, cy = largura // 2, altura // 2 - 20
    for r in range(180, 0, -6):  # brilho dourado
        alpha = 1 - r / 180
        c = (int(217 * alpha * .35), int(164 * alpha * .35), int(65 * alpha * .35))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(min(255, img.getpixel((cx, cy - r + 1))[i] + c[i]) for i in range(3)))
    ouro = (217, 164, 65)
    draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill=ouro)
    draw.polygon([(cx - 16, cy + 20), (cx + 16, cy + 20), (cx + 28, cy + 110), (cx - 28, cy + 110)], fill=ouro)
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(13, 16, 23))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = 'Cria dados de demonstração e o usuário admin / enigma123.'

    def handle(self, *args, **options):
        faltando = []
        for app, modelo in APPS_NECESSARIOS:
            try:
                apps.get_model(app, modelo)
            except LookupError:
                faltando.append(app)
        if faltando:
            raise CommandError('Instale primeiro estes apps (settings.py e urls.py): ' + ', '.join(faltando))

        Sala = apps.get_model('salas', 'Sala')
        if Sala.objects.exists():
            self.stdout.write(self.style.WARNING('Já existem dados. Para recomeçar, apague o db.sqlite3 e rode migrate de novo.'))
            return

        Tema = apps.get_model('temas', 'Tema')
        Jogo = apps.get_model('jogos', 'Jogo')
        Horario = apps.get_model('horarios', 'Horario')
        Cliente = apps.get_model('clientes', 'Cliente')
        Funcionario = apps.get_model('funcionarios', 'Funcionario')
        Participante = apps.get_model('participantes', 'Participante')
        Grupo = apps.get_model('grupos', 'Grupo')
        Agendamento = apps.get_model('agendamentos', 'Agendamento')
        Pagamento = apps.get_model('pagamentos', 'Pagamento')
        Sessao = apps.get_model('sessoes', 'Sessao')
        Avaliacao = apps.get_model('avaliacoes', 'Avaliacao')

        random.seed(7)
        hoje = timezone.localdate()

        # Usuário para entrar no sistema
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@enigma.com', 'enigma123', first_name='Admin', last_name='Enigma')

        # Salas
        dados_salas = [
            ('O Laboratório do Dr. Voss', 'Você acorda trancado em um laboratório abandonado. O cientista deixou pistas, mas o tempo está acabando.', 2, 6, 60, '65.00', ((20, 26, 48), (40, 30, 70))),
            ('A Cripta Esquecida', 'Uma cripta antiga guarda um segredo proibido. Símbolos, velas e passagens secretas testam a coragem do grupo.', 3, 8, 75, '70.00', ((30, 18, 20), (58, 30, 24))),
            ('Expresso do Oriente', 'Um crime a bordo de um trem de luxo. Descubra o culpado antes da próxima estação.', 2, 5, 60, '60.00', ((16, 30, 36), (24, 54, 60))),
            ('Bunker 13', 'Um abrigo subterrâneo, um sistema falhando e 90 minutos para evitar o desastre.', 4, 8, 90, '75.00', ((18, 22, 18), (36, 48, 30))),
        ]
        salas = []
        for nome, desc, cmin, cmax, dur, valor, cores in dados_salas:
            sala = Sala.objects.create(nome=nome, descricao=desc, capacidade_minima=cmin, capacidade_maxima=cmax,
                                       duracao_minutos=dur, valor_base=valor)
            img = gerar_imagem(*cores)
            if img:
                sala.imagem.save(f'sala_{sala.pk}.jpg', img, save=True)
            salas.append(sala)

        # Temas
        temas = [
            Tema.objects.create(nome='Terror', descricao='Sustos, escuridão e tensão constante.', faixa_etaria_minima=14, classificacao='14', ambientacao='Luz baixa, sons de fundo, névoa'),
            Tema.objects.create(nome='Mistério', descricao='Investigação, pistas e muita dedução.', faixa_etaria_minima=10, classificacao='10', ambientacao='Cenário de época, música clássica'),
            Tema.objects.create(nome='Ficção científica', descricao='Tecnologia, laboratórios e futuros incertos.', faixa_etaria_minima=12, classificacao='12', ambientacao='Luzes neon e painéis eletrônicos'),
            Tema.objects.create(nome='Aventura', descricao='Exploração e enigmas para toda a família.', faixa_etaria_minima=0, classificacao='livre', ambientacao='Cenário colorido'),
        ]

        # Jogos (sala, tema, nível, tempo, pontos, adicional)
        dados_jogos = [
            ('O Experimento', 'Um experimento saiu do controle. Encontre o antídoto antes que o laboratório seja selado.', 4, 60, 1000, '10.00', 0, 2, ['10:00', '12:30']),
            ('A Maldição da Cripta', 'Quem entra na cripta nunca mais sai... a não ser que decifre a maldição.', 5, 75, 1500, '15.00', 1, 0, ['14:00', '16:30']),
            ('Assassinato no Expresso', 'Um passageiro foi encontrado morto. Todos são suspeitos.', 3, 60, 1000, '5.00', 2, 1, ['14:00', '16:00']),
            ('Protocolo 13', 'O reator do bunker está instável. Reinicie o sistema em 90 minutos.', 4, 90, 2000, '12.00', 3, 2, ['18:00', '20:00']),
            ('Tesouro do Capitão', 'Uma caça ao tesouro leve e divertida para a família toda.', 2, 60, 800, '0.00', 0, 3, ['16:00', '18:30']),
        ]
        jogos = []
        for nome, hist, nivel, tempo, pts, adic, i_sala, i_tema, _ in dados_jogos:
            jogos.append(Jogo.objects.create(
                nome=nome, historia=hist, nivel_dificuldade=nivel, tempo_limite_minutos=tempo,
                pontuacao_maxima=pts, valor_adicional=adic, sala=salas[i_sala], tema=temas[i_tema],
                instrucoes='Trabalhem em equipe e comuniquem tudo que encontrarem.'))

        # Horários: 3 dias passados (para sessões concluídas) e os próximos 7 dias
        horarios = []
        for jogo, (_, _, _, _, _, _, _, _, slots) in zip(jogos, dados_jogos):
            for delta in range(-3, 8):
                dia = hoje + timedelta(days=delta)
                for hora in slots:
                    h, m = map(int, hora.split(':'))
                    horarios.append(Horario.objects.create(
                        jogo=jogo, data=dia, hora_inicio=datetime(2000, 1, 1, h, m).time(),
                        status='encerrado' if delta < 0 else 'disponivel'))

        # Equipe
        funcionarios = [
            Funcionario.objects.create(nome='Rafael Mendes', email='rafael@enigma.com', telefone='(11) 91111-1111', cargo='game_master', data_admissao=date(2024, 3, 10), salario=3200.0, matricula='F001'),
            Funcionario.objects.create(nome='Beatriz Costa', email='bia@enigma.com', telefone='(11) 92222-2222', cargo='game_master', data_admissao=date(2025, 1, 15), salario=3000.0, matricula='F002'),
            Funcionario.objects.create(nome='Henrique Alves', email='henrique@enigma.com', telefone='(11) 93333-3333', cargo='gerente', data_admissao=date(2023, 6, 1), salario=5200.0, matricula='F003'),
        ]

        # Clientes
        clientes = [
            Cliente.objects.create(nome=n, email=e, telefone=t, cpf=c, cidade=ci, data_nascimento=date(1990 + i, 3 + i, 10 + i))
            for i, (n, e, t, c, ci) in enumerate([
                ('Marina Souza', 'marina@email.com', '(11) 98888-0001', '111.111.111-11', 'São Paulo'),
                ('João Pedro Lima', 'joao@email.com', '(11) 98888-0002', '222.222.222-22', 'Guarulhos'),
                ('Carla Nogueira', 'carla@email.com', '(11) 98888-0003', '333.333.333-33', 'Santo André'),
                ('Tiago Ramos', 'tiago@email.com', '(11) 98888-0004', '444.444.444-44', 'São Paulo'),
                ('Fernanda Dias', 'fernanda@email.com', '(11) 98888-0005', '555.555.555-55', 'Osasco'),
                ('Lucas Pereira', 'lucas@email.com', '(11) 98888-0006', '666.666.666-66', 'São Paulo'),
            ])
        ]

        # Participantes
        nomes_part = ['Ana Beatriz', 'Bruno Carvalho', 'Camila Torres', 'Diego Martins', 'Elisa Prado', 'Felipe Rocha', 'Gabriela Luz', 'Heitor Nunes']
        participantes = []
        for i, nome in enumerate(nomes_part):
            nasc = date(2012, 5, 5) if i == 7 else date(1995 + i % 5, 1 + i, 12)
            participantes.append(Participante.objects.create(
                nome=nome, email=f'{nome.split()[0].lower()}@email.com', documento=f'MG-{1000 + i}', data_nascimento=nasc))

        # Grupos (muitos-para-muitos com participantes)
        g1 = Grupo.objects.create(nome='Os Decifradores', tipo_grupo='amigos', tamanho_estimado=4, cliente=clientes[0])
        g1.participantes.set(participantes[:4])
        g2 = Grupo.objects.create(nome='Família Lima', tipo_grupo='familia', tamanho_estimado=5, cliente=clientes[1])
        g2.participantes.set(participantes[3:8])
        g3 = Grupo.objects.create(nome='Equipe TechCorp', tipo_grupo='empresa', tamanho_estimado=6, cliente=clientes[2])
        g3.participantes.set(participantes[1:6])

        def achar(jogo, delta, hora):
            h, m = map(int, hora.split(':'))
            return Horario.objects.get(jogo=jogo, data=hoje + timedelta(days=delta), hora_inicio=datetime(2000, 1, 1, h, m).time())

        # Reservas passadas (viram sessões concluídas)
        passadas = [
            (clientes[0], jogos[0], -2, '10:00', 4, g1, 'concluido'),
            (clientes[3], jogos[2], -1, '14:00', 3, None, 'concluido'),
            (clientes[4], jogos[3], -3, '18:00', 5, None, 'concluido'),
        ]
        sessoes = []
        for i, (cli, jogo, delta, hora, qtd, grupo, st) in enumerate(passadas):
            ag = Agendamento.objects.create(cliente=cli, horario=achar(jogo, delta, hora), quantidade_pessoas=qtd,
                                            grupo=grupo, status='confirmado', desconto=0)
            Pagamento.objects.create(agendamento=ag, valor=ag.valor_total, metodo='pix', status='pago')
            inicio = timezone.make_aware(datetime.combine(hoje + timedelta(days=delta), ag.horario.hora_inicio))
            s = Sessao.objects.create(agendamento=ag, funcionario=funcionarios[i % 2], status='concluida',
                                      resultado='escapou' if i != 1 else 'nao_escapou',
                                      inicio_real=inicio, fim_real=inicio + timedelta(minutes=jogo.tempo_limite_minutos - 7),
                                      pontuacao_final=int(jogo.pontuacao_maxima * (0.9 - i * 0.2)))
            sessoes.append(s)

        # Avaliações
        Avaliacao.objects.create(cliente=clientes[0], sessao=sessoes[0], nota=5, nota_atendimento=5, comentario='Experiência incrível! Os enigmas são muito bem pensados.', recomendaria=True, resposta_empresa='Obrigado, Marina! Esperamos vocês em breve.')
        Avaliacao.objects.create(cliente=clientes[3], sessao=sessoes[1], nota=4, nota_atendimento=5, comentario='Divertido, mas o tempo foi curto para nós.', recomendaria=True)
        Avaliacao.objects.create(cliente=clientes[4], sessao=sessoes[2], nota=5, nota_atendimento=4, comentario='O Bunker 13 é o melhor cenário!', recomendaria=True)

        # Reservas futuras
        futuras = [
            (clientes[1], jogos[1], 1, '14:00', 5, g2, 'pago'),
            (clientes[2], jogos[3], 2, '18:00', 6, g3, 'parcial'),
            (clientes[5], jogos[0], 1, '12:30', 2, None, 'pendente'),
            (clientes[0], jogos[4], 3, '16:00', 4, g1, 'pago'),
            (clientes[3], jogos[2], 4, '16:00', 3, None, 'cancelar'),
        ]
        for cli, jogo, delta, hora, qtd, grupo, pg in futuras:
            ag = Agendamento.objects.create(cliente=cli, horario=achar(jogo, delta, hora), quantidade_pessoas=qtd,
                                            grupo=grupo, desconto=10 if qtd >= 6 else 0)
            if pg == 'pago':
                Pagamento.objects.create(agendamento=ag, valor=ag.valor_total, metodo='cartao_credito', status='pago')
            elif pg == 'parcial':
                Pagamento.objects.create(agendamento=ag, valor=round(ag.valor_total / 2, 2), metodo='pix', status='pago')
            elif pg == 'pendente':
                Pagamento.objects.create(agendamento=ag, valor=ag.valor_total, metodo='dinheiro', status='pendente')
            elif pg == 'cancelar':
                ag.status = 'cancelado'
                ag.save()

        self.stdout.write(self.style.SUCCESS('Dados de demonstração criados!'))
        self.stdout.write('Entre com usuário: admin   senha: enigma123')
