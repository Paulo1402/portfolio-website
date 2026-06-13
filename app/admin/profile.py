from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from app.models import Profile


class ProfileAdmin(TranslationAdmin):
    fieldsets = (
        ("Profile Information", {"fields": ("description", "picture")}),
        ("Contact", {"fields": ("email", "linkedin", "github")}),
    )
    # list_display = ("email", "linkedin", "github", "created_at", "updated_at")

    def has_add_permission(self, request):
        if Profile.objects.exists():
            return False

        return super().has_add_permission(request)


admin.site.register(Profile, ProfileAdmin)
