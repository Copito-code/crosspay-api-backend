"""
Django settings for config project.
...
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url # Nuevo: Para configurar PostgreSQL con una URL


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = ['*']

# En producción, permitimos todos los subdominios y la URL principal.
if not DEBUG:
    # Agrega la URL explícitamente y el comodín de Render en produccion
    ALLOWED_HOSTS = ['crosspay-api-backend.onrender.com', '.onrender.com']


# --------------------------------------------------------------------------
# 💥 CORRECCIÓN DEFINITIVA DE CORS/CSRF
# --------------------------------------------------------------------------

# Orígenes permitidos de CORS. Se establece una lista explícita y completa como valor por defecto.
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS', 
    # **AQUÍ FORZAMOS TODOS LOS ORÍGENES NECESARIOS**
    default='http://localhost:5173,http://127.0.0.1:5173,https://crosspay-api-backend.onrender.com'
).split(',')


if DEBUG:
    # En desarrollo local (si DEBUG=True), permitimos *cualquier* origen (más flexible).
    CORS_ALLOW_ALL_ORIGINS = True
    # Si usamos ALLOW_ALL_ORIGINS, la lista CORS_ALLOWED_ORIGINS se ignora, 
    # pero la dejamos para que sirva de default en producción si la variable env falla.
else:
    # En producción (Render, si DEBUG=False), solo se permiten los de la lista de arriba.
    CORS_ALLOW_ALL_ORIGINS = False 

CORS_ALLOW_CREDENTIALS = True 

# Esto le dice a Django que confíe en los orígenes que envían la cookie CSRF.
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173', 
    'http://127.0.0.1:5173',
    'https://crosspay-api-backend.onrender.com', 
]

# ⚠️ La variable CORS_ORIGIN_WHITELIST es obsoleta. No la definimos para evitar conflictos.

# --------------------------------------------------------------------------
# FIN CORRECCIÓN DE CORS/CSRF
# --------------------------------------------------------------------------


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Para la api Rest 
    'corsheaders',  # Para permitir la comunicación con React
    'transactions', # Nuestra aplicación de transacciones'
    'rest_framework_simplejwt', # Autenticación
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 1. CRUCIAL: Debe ser la primera después de WhiteNoise
    'django.middleware.security.SecurityMiddleware', # 2
    'django.contrib.sessions.middleware.SessionMiddleware', # 3 
    'django.middleware.common.CommonMiddleware', # 4
    'django.middleware.csrf.CsrfViewMiddleware', # 5
    'django.contrib.auth.middleware.AuthenticationMiddleware', #6 
    'django.contrib.messages.middleware.MessageMiddleware', # 7
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 8
    
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///db.sqlite3',
        cast=dj_database_url.parse
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Habilitar compresión de archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuración de Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Usa JWT en lugar de SessionAuthentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
         # Asegura que el acceso es privado por defecto
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# --- Configuración de Cookies y Headers ---

SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SAMESITE = None 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False


CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken', 
    'x-requested-with',
]