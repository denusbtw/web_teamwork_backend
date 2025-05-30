# Generated by Django 5.2.1 on 2025-05-26 08:47

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "title",
                    models.CharField(help_text="Title of category.", max_length=255),
                ),
                ("slug", models.SlugField(help_text="Slug of category.", unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Hackathon",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "title",
                    models.CharField(help_text="Title of hackathon", max_length=255),
                ),
                (
                    "description",
                    models.CharField(
                        help_text="Description of hackathon.", max_length=2000
                    ),
                ),
                (
                    "prize",
                    models.PositiveIntegerField(help_text="Prize for hackathon."),
                ),
                ("image", models.ImageField(upload_to="images/hackathons")),
                (
                    "start_datetime",
                    models.DateTimeField(help_text="Start date and time of hackathon."),
                ),
                (
                    "end_datetime",
                    models.DateTimeField(help_text="End date and time of hackathon."),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Category of hackathon.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="hackathons",
                        to="hackathons.category",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Winner of the hackathon.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="won_hackathons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Participant",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("active", "Active"),
                            ("pending", "Pending"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        help_text="Current participation status of the user in the hackathon.",
                    ),
                ),
                (
                    "hackathon",
                    models.ForeignKey(
                        help_text="Hackathon the user has applied to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hackathons.hackathon",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User who applied to participate in the hackathon.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
