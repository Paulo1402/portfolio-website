from django.contrib import admin

from app.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Profile Information", {"fields": ("description", "picture")}),
        ("Contact", {"fields": ("email", "linkedin", "github")}),
    )
    # list_display = ("email", "linkedin", "github", "created_at", "updated_at")


admin.site.register(Profile, ProfileAdmin)
