import os

import dj_database_url

from .base import *

ALLOWED_HOSTS = ["web-teamwork-backend.onrender.com"]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}
