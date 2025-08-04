from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-uu_c31*jf#7ndo)yl-#96&n!fd*q09bbda+93(7+$cv_klk4_y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Liste des hôtes autorisés
ALLOWED_HOSTS = [
    '10.134.84.41',    # Votre adresse IP locale
    'localhost',
    '127.0.0.1',
    '0.0.0.0',         # Pour les conteneurs Docker
    '::1',             # IPv6 localhost
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'api_app',
    'web_app',
    'account',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Doit être placé le plus haut possible
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

AUTH_USER_MODEL = 'web_app.Utilisateur'

# CORS Configuration
# En développement, on autorise toutes les origines
CORS_ALLOW_ALL_ORIGINS = True  # À désactiver en production
CORS_ALLOW_CREDENTIALS = True

# Liste des origines autorisées (en plus de CORS_ALLOW_ALL_ORIGINS)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',         # React dev server
    'http://10.134.84.41:8000',          # Android Emulator to localhost

]

# Autoriser les en-têtes personnalisés
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
    'cache-control',
    'expires',
    'pragma',
]

# Méthodes HTTP autorisées
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# En-têtes exposés au client
CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
    'authorization',
    'content-disposition',
]

# Configuration CSRF pour le développement
CSRF_TRUSTED_ORIGINS = [
    # Développement local
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    
    # Développement mobile
    'http://10.134.84.41:8000',
    
    # Android
    'http://10.134.84.41:8000',
]

# Configuration des sessions et cookies
SESSION_COOKIE_AGE = 1209600  # 2 semaines en secondes
SESSION_COOKIE_SAMESITE = 'Lax'  # 'Lax' est plus sécurisé que 'None' mais fonctionne avec la plupart des cas d'usage
SESSION_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS
SESSION_COOKIE_HTTPONLY = True  # Empêche l'accès JavaScript au cookie de session
SESSION_SAVE_EVERY_REQUEST = True  # Rafraîchir le cookie de session à chaque requête

# Configuration CSRF
CSRF_COOKIE_HTTPONLY = False  # Doit être False pour permettre l'accès depuis JavaScript
CSRF_COOKIE_SECURE = False    # Mettre à True en production avec HTTPS
CSRF_COOKIE_SAMESITE = 'Lax'  # 'Lax' est recommandé pour la compatibilité
CSRF_USE_SESSIONS = False     # Stocker le token CSRF dans un cookie plutôt que dans la session

# Configuration des en-têtes de sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration CORS avancée
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

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
    'cache-control',
    'expires',
    'pragma',
    'accept-language',
]

CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
    'authorization',
    'content-disposition',
]

# JWT Settings
from datetime import timedelta

# Swagger/OpenAPI settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Durée de vie du token d'accès (7 jours)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Durée de vie du token de rafraîchissement (30 jours)
    'ROTATE_REFRESH_TOKENS': True,  # Génère un nouveau token de rafraîchissement à chaque rafraîchissement
    'BLACKLIST_AFTER_ROTATION': True,  # Ajoute les anciens tokens à une liste noire après rotation
    'UPDATE_LAST_LOGIN': True,  # Met à jour le dernier login de l'utilisateur
    
    'ALGORITHM': 'HS256',  # Algorithme de chiffrement
    'SIGNING_KEY': SECRET_KEY,  # Clé secrète utilisée pour signer les tokens
    'VERIFYING_KEY': None,  # Clé de vérification (None signifie qu'on utilise SIGNING_KEY)
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),  # Préfixe du token dans l'en-tête d'authentification
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Add your frontend's origin
    'http://10.30.247.41:8000',  # For mobile testing
]