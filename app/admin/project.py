import requests
import tagulous.admin
from django.contrib import admin, messages
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.urls import path

from app.models import ProjectImage, Project


class ImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    # TODO: use pillow to resize project images to the same proportion

    list_display = ("title", "github_url", "fetch_github_button")
    inlines = [ImageInline]

    def fetch_github_button(self, obj):
        return format_html(
            '<a href="{}" class="button">Fetch Github</a>',
            f"/admin/app/project/{obj.id}/fetch-github/",
        )

    fetch_github_button.short_description = "Fetch Github"
    fetch_github_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/fetch-github/",
                self.admin_site.admin_view(self.fetch_github),
            )
        ]

        return custom_urls + urls

    def fetch_github(self, request, object_id):
        project = get_object_or_404(Project, id=object_id)
        project_name = project.github_url.replace("https://github.com/", "")

        response = requests.get(
            f"https://api.github.com/repos/{project_name}",
            headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}"},
        )

        if response.ok:
            response_json = response.json()
            topics = response_json["topics"]

            project.topics = topics

            self.message_user(
                request,
                "Github data and images updated!",
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                "Failed to fetch Github data!",
                level=messages.ERROR,
            )

        return redirect("/admin/app/project/")


tagulous.admin.register(Project, ProjectAdmin)
