from django.contrib import admin
from django.utils.html import format_html

from app.models import Project


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def fetch_github_button(self, obj):
        print(obj, type(obj))
        return format_html(
            '<a href="{}" class="button">Fetch Github</a>',
        )

    fetch_github_button.short_description = "Fetch Github"
    fetch_github_button.allow_tags = True
