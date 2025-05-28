from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from web_teamwork.core.models import UUIDModel


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = email.lower()
        email = self.normalize_email(email)

        if username is None or username.strip() == "":
            username = self.generate_username_from_email(email)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")

        return self.create_user(email, password, username, **extra_fields)

    def generate_username_from_email(self, email):
        local = email.split("@")[0]
        return f"{local}_{get_random_string(6)}"


class User(UUIDModel, AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        HOST = ("host", "Host")
        USER = ("user", "User")

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    role = models.CharField(
        default=Role.USER,
        choices=Role.choices,
        blank=True,
        help_text=_("Role of user."),
    )

    profile_picture = models.ImageField(
        upload_to="images/profile_pictures",
        blank=True,
        null=True,
        help_text=_("Profile picture of user."),
    )
    profile_background = models.ImageField(
        upload_to="images/profile_backgrounds",
        blank=True,
        null=True,
        help_text=_("Profile background of user."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_host(self):
        return self.role == self.Role.HOST
