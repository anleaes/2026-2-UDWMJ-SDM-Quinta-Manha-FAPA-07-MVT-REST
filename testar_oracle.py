"""
Testa a conexão com o Oracle Cloud (OCI) usando os dados do seu .env.
Uso:  python testar_oracle.py
Ele NÃO altera nada no banco: só conecta e mostra a versão.
"""
import os
import re
import sys
from pathlib import Path

from decouple import config

BASE = Path(__file__).resolve().parent


def ok(msg):
    print('  [OK]   ' + msg)


def erro(msg):
    print('  [ERRO] ' + msg)


print('=== Teste de conexão Oracle (ENIGMA) ===')
usuario = config('DB_USER', default='')
senha = config('DB_PASSWORD', default='')
tns_name = config('TNS_NAME', default='')
wallet_senha = config('WALLET_PASSWORD', default='')
tns_admin = Path(config('TNS_ADMIN', default='Wallet_escaperoomdb'))
if not tns_admin.is_absolute():
    tns_admin = (BASE / tns_admin).resolve()

problemas = 0
print('\n1) Conferindo o .env')
for nome, valor in (('DB_USER', usuario), ('DB_PASSWORD', senha), ('TNS_NAME', tns_name),
                    ('WALLET_PASSWORD', wallet_senha)):
    if valor:
        ok(f'{nome} preenchido')
    else:
        erro(f'{nome} está vazio no .env'); problemas += 1

print('\n2) Conferindo a pasta do Wallet')
print(f'   Pasta: {tns_admin}')
if not tns_admin.is_dir():
    erro('A pasta do Wallet não existe. Descompacte o zip do Wallet na raiz do projeto '
         'e ajuste TNS_ADMIN no .env para o nome da pasta.'); problemas += 1
else:
    for arquivo in ('tnsnames.ora', 'sqlnet.ora'):
        if (tns_admin / arquivo).exists():
            ok(arquivo + ' encontrado')
        else:
            erro(arquivo + ' NÃO encontrado (a pasta está certa? às vezes o zip cria uma pasta dentro de outra)')
            problemas += 1
    if (tns_admin / 'ewallet.pem').exists():
        ok('ewallet.pem encontrado (necessário para o modo simples do python-oracledb)')
    else:
        erro('ewallet.pem NÃO encontrado'); problemas += 1
    tns = tns_admin / 'tnsnames.ora'
    if tns.exists():
        nomes = re.findall(r'^([A-Za-z0-9_\-]+)\s*=', tns.read_text(errors='ignore'), re.M)
        print('   Serviços disponíveis no Wallet: ' + ', '.join(nomes))
        if tns_name and tns_name not in nomes:
            erro(f'TNS_NAME="{tns_name}" não está na lista acima. Use um dos nomes listados.'); problemas += 1

if problemas:
    print(f'\nCorrija os {problemas} problema(s) acima e rode de novo.')
    sys.exit(1)

print('\n3) Conectando ao Oracle...')
try:
    import oracledb
except ImportError:
    erro('oracledb não instalado. Rode: pip install -r requirements.txt'); sys.exit(1)

try:
    conexao = oracledb.connect(user=usuario, password=senha, dsn=tns_name,
                               config_dir=str(tns_admin), wallet_location=str(tns_admin),
                               wallet_password=wallet_senha)
    cursor = conexao.cursor()
    cursor.execute("select banner from v$version where rownum = 1")
    ok('Conectou! ' + str(cursor.fetchone()[0]))
    cursor.execute('select user from dual')
    ok('Usuário conectado: ' + str(cursor.fetchone()[0]))
    conexao.close()
    print('\nTudo certo. Pode usar DB_ENGINE=oracle no .env.')
except Exception as e:  # noqa
    msg = str(e)
    erro(msg)
    if 'ORA-01017' in msg:
        print('   Dica: usuário ou senha do BANCO errados (DB_USER / DB_PASSWORD).')
    elif 'DPY-6005' in msg or 'timed out' in msg.lower() or 'DPY-6000' in msg:
        print('   Dica: não alcançou o servidor. Veja a internet/VPN/firewall e se o banco OCI está ligado. '
              'Se o banco só aceita IPs liberados (ACL), peça ao dono para liberar o seu.')
    elif 'DPY-4' in msg or 'wallet' in msg.lower() or 'pem' in msg.lower():
        print('   Dica: confira WALLET_PASSWORD (senha escolhida ao baixar o Wallet) e a pasta do Wallet.')
    elif 'DPY-6001' in msg or 'ORA-12514' in msg or 'ORA-12154' in msg:
        print('   Dica: TNS_NAME errado. Use um dos serviços listados no passo 2.')
    sys.exit(1)
