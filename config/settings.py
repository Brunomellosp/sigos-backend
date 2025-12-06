from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv  # <- usa python-dotenv
from core.utils.env import get_env, get_env_bool, get_env_list

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env que está na raiz (mesmo nível do manage.py)
load_dotenv(BASE_DIR / ".env")

# Django
SECRET_KEY = get_env("DJANGO_SECRET_KEY")
DEBUG = get_env_bool("DJANGO_DEBUG")
ALLOWED_HOSTS = get_env_list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "corsheaders",

    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Banco de dados
if DEBUG:
    # DEV: SQLite local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # PROD: PostgreSQL (Supabase, etc.)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": get_env("DB_NAME"),
            "USER": get_env("DB_USER"),
            "PASSWORD": get_env("DB_PASSWORD"),
            "HOST": get_env("DB_HOST"),
            "PORT": get_env("DB_PORT"),
        }
    }



AUTH_USER_MODEL = "core.User"

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
            "django_filters.rest_framework.DjangoFilterBackend",
            "rest_framework.filters.SearchFilter",
            "rest_framework.filters.OrderingFilter",
    ),
}

from rest_framework_simplejwt.settings import api_settings as jwt_api_settings

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(get_env("JWT_ACCESS_TOKEN_LIFETIME_MIN"))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(get_env("JWT_REFRESH_TOKEN_LIFETIME_DAYS"))
    ),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_env("EMAIL_HOST")
EMAIL_PORT = int(get_env("EMAIL_PORT"))
EMAIL_HOST_USER = get_env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = get_env_bool("EMAIL_USE_TLS")

CORS_ALLOWED_ORIGINS = get_env_list("CORS_ALLOWED_ORIGINS")
