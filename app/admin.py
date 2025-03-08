import requests
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html
from django.urls import path
from django.conf import settings
import tagulous.admin

from app.models import (
    Project,
    Skill,
    SkillArea,
    Profile,
    Formation,
    Image,
    Certification,
    Experience,
    Topic,
)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
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


class FormationAdmin(admin.ModelAdmin):
    pass


tagulous.admin.register(Formation, FormationAdmin)


class CertificationAdmin(admin.ModelAdmin):
    pass


tagulous.admin.register(Certification, CertificationAdmin)


class ExperienceAdmin(admin.ModelAdmin):
    pass


tagulous.admin.register(Experience, ExperienceAdmin)


@admin.register(Topic)
class TopicAdmin(tagulous.admin.TagModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "show")


@admin.register(SkillArea)
class SkillAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "index", "show")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
