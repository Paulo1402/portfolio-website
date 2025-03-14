from django.contrib import admin

from app.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Profile Information", {"fields": ("description", "picture")}),
        ("Contact", {"fields": ("email", "linkedin", "github")}),
    )


admin.site.register(Profile, ProfileAdmin)
