from django.urls import reverse_lazy

from pathlib import Path

from autosecretkey import AutoSecretKey

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = AutoSecretKey(BASE_DIR / "config.ini",
                            template=BASE_DIR / "config.dist.ini")

SECRET_KEY = CONFIG_FILE.secret_key
DEBUG = CONFIG_FILE.config["KEYLOG"]["Debug"]

ALLOWED_HOSTS = ["*"]

SECURE_PROXY_SSL_HEADER_NAME = CONFIG_FILE.config.get("KEYLOG", "SSLHeaderName", fallback="HTTP_X_FORWARDED_PROTO")
SECURE_PROXY_SSL_HEADER_VALUE = CONFIG_FILE.config.get("KEYLOG", "SSLHeaderValue", fallback="https")
SECURE_PROXY_SSL_HEADER = (SECURE_PROXY_SSL_HEADER_NAME, SECURE_PROXY_SSL_HEADER_VALUE)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mozilla_django_oidc',
    'ajax_datatable',
    'crispy_forms',

    'core',
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

ROOT_URLCONF = 'keylog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "frontend" / "templates" ],
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

WSGI_APPLICATION = 'keylog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "core.User"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

if "OIDC" in CONFIG_FILE.config:
    AUTHENTICATION_BACKENDS = [
        'core.backends.OIDCBackend',
    ]

    LOGIN_URL = reverse_lazy("oidc_authentication_init")

    OIDC_NAME = CONFIG_FILE.config.get("OIDC", "Name", fallback="OIDC")
    OIDC_RP_CLIENT_ID = CONFIG_FILE.config["OIDC"]["ClientID"]
    OIDC_RP_CLIENT_SECRET = CONFIG_FILE.config["OIDC"]["ClientSecret"]
    OIDC_OP_JWKS_ENDPOINT = CONFIG_FILE.config["OIDC"]["JWKS"]
    OIDC_OP_AUTHORIZATION_ENDPOINT = CONFIG_FILE.config["OIDC"]["Authorization"]
    OIDC_OP_TOKEN_ENDPOINT = CONFIG_FILE.config["OIDC"]["Token"]
    OIDC_OP_USER_ENDPOINT = CONFIG_FILE.config["OIDC"]["UserInfo"]
    OIDC_CREATE_USER = CONFIG_FILE.config.getboolean("OIDC", "CreateUsers", fallback=False)
    OIDC_RP_SIGN_ALGO = CONFIG_FILE.config.get("OIDC", "Algorithm", fallback="RS256")

    MIDDLEWARE.append("mozilla_django_oidc.middleware.SessionRefresh")

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "frontend/static/",
]

STATIC_URL = '/static/'

STATIC_ROOT = None if DEBUG else CONFIG_FILE.config.get("RESTOROO", "StaticRoot", fallback=BASE_DIR / "static")

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "/"

if "S3" in CONFIG_FILE.config:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    AWS_ACCESS_KEY_ID = CONFIG_FILE.config.get("S3", "AccessKey")
    AWS_SECRET_ACCESS_KEY = CONFIG_FILE.config.get("S3", "SecretKey")
    AWS_STORAGE_BUCKET_NAME = CONFIG_FILE.config.get("S3", "Bucket")
    AWS_S3_ENDPOINT_URL = CONFIG_FILE.config.get("S3", "Endpoint")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
