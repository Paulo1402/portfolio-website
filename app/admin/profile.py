from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from app.models import Profile


class ProfileAdmin(TranslationAdmin):
    fieldsets = (
        ("Profile Information", {"fields": ("description", "picture")}),
        ("Contact", {"fields": ("email", "linkedin", "github")}),
    )
    # list_display = ("email", "linkedin", "github", "created_at", "updated_at")


admin.site.register(Profile, ProfileAdmin)
