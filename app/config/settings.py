import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "clave-de-laboratorio-no-usar-en-produccion")
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = ["api"]
MIDDLEWARE = []
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_TZ = True

DATABASES = {}
DB_HOST = os.environ.get("DB_HOST", "")
if DB_HOST:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "travelroad"),
            "USER": os.environ.get("DB_USER", "alumno"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "CAMBIAR_ESTO"),
            "HOST": DB_HOST,
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

APP_DATA_DIR = Path(os.environ.get("APP_DATA_DIR", BASE_DIR / "data"))