from django.contrib import admin

from web_teamwork.hackathons.models import Hackathon, Category, Participant


@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "hackathon__title", "user__email", "status")
