from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from web_teamwork.core.models import UUIDModel, TimestampedModel

User = get_user_model()


class Category(UUIDModel, TimestampedModel):
    title = models.CharField(max_length=255, help_text=_("Title of category."))
    slug = models.SlugField(blank=True, unique=True, help_text=_("Slug of category."))

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Hackathon(UUIDModel, TimestampedModel):
    title = models.CharField(max_length=255, help_text=_("Title of hackathon"))
    description = models.CharField(
        max_length=2000, help_text=_("Description of hackathon.")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hackathons",
        help_text=_("Category of hackathon."),
    )
    prize = models.PositiveIntegerField(help_text=_("Prize for hackathon."))
    image = models.ImageField(upload_to="images/hackathons")
    start_datetime = models.DateTimeField(
        help_text=_("Start date and time of hackathon.")
    )
    end_datetime = models.DateTimeField(help_text=_("End date and time of hackathon."))
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_hackathons",
        help_text=_("Winner of the hackathon."),
    )
    hosted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_hackathons",
        help_text=_("The user who hosted this hackathon."),
    )
    # TODO: add location, rules fields

    def __str__(self):
        return self.title


class Participant(UUIDModel, TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = ("active", "Active")
        PENDING = ("pending", "Pending")
        REJECTED = ("rejected", "Rejected")
        COMPLETED = ("completed", "Completed")

    hackathon = models.ForeignKey(
        Hackathon,
        on_delete=models.CASCADE,
        related_name="participants",
        help_text=_("Hackathon the user has applied to."),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hackathons",
        help_text=_("User who applied to participate in the hackathon."),
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.PENDING,
        blank=True,
        help_text=_("Current participation status of the user in the hackathon."),
    )
