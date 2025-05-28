import os

from .base import *

env.read_env(str(BASE_DIR / ".env.production"))

ALLOWED_HOSTS = ["localhost"]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG")

DATABASES = {"default": env.db("DATABASE_URL")}
