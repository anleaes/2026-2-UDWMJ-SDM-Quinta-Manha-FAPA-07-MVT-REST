"""
Configurações do projeto Escape Room (Django 5.2).

Dados sensíveis (chave secreta, senha do banco) ficam no arquivo .env,
que NUNCA vai para o GitHub. Veja o .env.example.
"""
import os
import sys
from pathlib import Path

from decouple import config

# Raiz do projeto (onde fica o manage.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pasta onde ficam os APPs do projeto (um app para cada entidade)
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(0, APPS_DIR)

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Apps instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --- APPS DO PROJETO ---
    # Cada pessoa remove o "#" somente da linha do(s) seu(s) app(s).

    # 'core.apps.CoreConfig',

    # 'accounts.apps.AccountsConfig',

    # 'pessoas.apps.PessoasConfig',

    # 'clientes.apps.ClientesConfig',

    # 'funcionarios.apps.FuncionariosConfig',

    # 'participantes.apps.ParticipantesConfig',

    # 'salas.apps.SalasConfig',

    # 'temas.apps.TemasConfig',

    # 'jogos.apps.JogosConfig',

    # 'horarios.apps.HorariosConfig',

    # 'grupos.apps.GruposConfig',

    # 'agendamentos.apps.AgendamentosConfig',

    # 'pagamentos.apps.PagamentosConfig',

    # 'sessoes.apps.SessoesConfig',

    # 'avaliacoes.apps.AvaliacoesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'escaperoomapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # menu lateral e links do ENIGMA (veja escaperoomapp/context_processors.py)
                'escaperoomapp.context_processors.enigma',
            ],
        },
    },
]

WSGI_APPLICATION = 'escaperoomapp.wsgi.application'


# Banco de dados
# DB_ENGINE=sqlite  -> banco local, usado no dia a dia de cada pessoa
# DB_ENGINE=oracle  -> Oracle Cloud OCI (padrão, usado na versão final)
if config('DB_ENGINE', default='oracle') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # Pasta do Wallet do Oracle (caminho relativo à raiz do projeto)
    tns_admin = Path(config('TNS_ADMIN', default='Wallet_escaperoomdb'))
    if not tns_admin.is_absolute():
        tns_admin = (Path(BASE_DIR) / tns_admin).resolve()
    os.environ['TNS_ADMIN'] = str(tns_admin)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': config('TNS_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'OPTIONS': {
                'config_dir': str(tns_admin),
                'wallet_location': str(tns_admin),
                'wallet_password': config('WALLET_PASSWORD'),
            },
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internacionalização
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Arquivos estáticos (CSS, JavaScript e imagens do front-end)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

# Arquivos enviados por upload (fotos, documentos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
