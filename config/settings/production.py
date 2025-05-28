from .base import *

env.read_env(str(BASE_DIR / ".env.production"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG")

DATABASES = {"default": env.db("DATABASE_URL")}
