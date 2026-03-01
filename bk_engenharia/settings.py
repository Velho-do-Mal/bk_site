"""
BK Engenharia e Tecnologia — Django Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production-bk2024!')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,bk-engenharia.com,www.bk-engenharia.com').split(',')
CSRF_TRUSTED_ORIGINS = ['https://bk-engenharia.com', 'https://www.bk-engenharia.com']

# ── Aplicações ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Terceiros
    'meta',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'crispy_tailwind',
    'rosetta',

    # Apps BK
    'apps.core',
    'apps.servicos',
    'apps.portfolio',
    'apps.loja',
    'apps.blog',
    'apps.contato',
    'apps.accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',        # i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bk_engenharia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.core.context_processors.site_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'bk_engenharia.wsgi.application'

# ── Banco de Dados ───────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    import urllib.parse as up
    r = up.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': r.path[1:],
            'USER': r.username,
            'PASSWORD': r.password,
            'HOST': r.hostname,
            'PORT': r.port or 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Internacionalização ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('pt-br', _('Português')),
    ('en', _('English')),
    ('es', _('Español')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# ── Arquivos Estáticos ───────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Auth ─────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LOGIN_URL = '/cliente/login/'
LOGIN_REDIRECT_URL = '/cliente/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'marcio@bk-engenharia.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'BK Engenharia <marcio@bk-engenharia.com>'
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'marcio@bk-engenharia.com')

# ── MercadoPago ───────────────────────────────────────────────────────────────
MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN', '')
MERCADOPAGO_PUBLIC_KEY = os.environ.get('MERCADOPAGO_PUBLIC_KEY', '')

# ── django-meta (SEO) ─────────────────────────────────────────────────────────
META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'bk-engenharia.com'
META_SITE_NAME = 'BK Engenharia e Tecnologia'
META_INCLUDE_KEYWORDS_TAG = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_DEFAULT_KEYWORDS = [
    'engenharia elétrica', 'subestações', 'linhas de transmissão',
    'projetos elétricos', 'BK Engenharia', 'ETAP', 'PLS-CADD', 'BIM',
    'engenharia curitiba', 'projetos subestações 230kV',
]

# ── CKEditor ──────────────────────────────────────────────────────────────────
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['Source'],
        ],
        'height': 400,
        'width': '100%',
    },
}

# ── Crispy Forms ──────────────────────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

# ── WhatsApp / Contato ────────────────────────────────────────────────────────
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '5541995275570')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
