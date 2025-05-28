from datetime import timedelta

from .base import *

env.read_env(BASE_DIR / ".env.local")

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG")

DATABASES = {"default": env.db("DATABASE_URL")}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=100),
}
