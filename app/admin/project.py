import io

import requests
import tagulous.admin
from django.contrib import admin, messages
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.urls import path
from PIL import Image

from app.forms.base import BaseStartDateEndDateForm
from app.models import ProjectImage, Project
from app.utils.image import convert_image_to_inmemoryfile


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    inlines = [ProjectImageInline]
    fieldsets = (
        ("Project Information", {"fields": ("title", "company", "description")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("github_url", "topics")}),
    )
    search_fields = ("title", "company")
    list_display = (
        "title",
        "company",
        "github_url",
        "fetch_github_button",
        "created_at",
        "updated_at",
    )

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

        try:
            response.raise_for_status()
            response_json = response.json()

            topics = response_json["topics"]
            old_topics = project.topics.tag_model.objects.all()

            project.topics = [*old_topics, *topics]

            images = self.fetch_project_images(project_name)

            for image, name in images:
                inmemory_image = convert_image_to_inmemoryfile(image, name)
                project_image = project.project_images.filter(
                    image__endswith=name
                ).first()

                # update the image if it exists
                if project_image:
                    project_image.image = inmemory_image
                else:
                    project.project_images.create(image=inmemory_image)

            project.save()

            self.message_user(
                request,
                "Github data and images updated!",
                level=messages.SUCCESS,
            )
        except Exception as e:
            print("Failed to fetch Github data!", e)

            self.message_user(
                request,
                "Failed to fetch Github data!",
                level=messages.ERROR,
            )

        return redirect("/admin/app/project/")

    def save_model(self, request, obj, form, change):
        # TODO: resize project images in order to have consistent dimensions

        super().save_model(request, obj, form, change)

    def fetch_project_images(
        self,
        project: str,
    ):
        project_images = []
        extensions_available = [".png", ".jpg", ".jpeg"]

        response = requests.get(
            f"https://api.github.com/repos/{project}/contents/.github",
            headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}"},
        )

        response.raise_for_status()
        response_json = response.json()

        for content in response_json:
            content_name = content["name"]
            is_image = any(
                [content_name.endswith(extension) for extension in extensions_available]
            )

            if is_image:
                img_url = content["download_url"]
                response = requests.get(
                    img_url,
                    headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}"},
                )

                if response.status_code == 200:
                    data = response.content
                    image = Image.open(io.BytesIO(data))

                    project_images.append((image, content_name))

        return project_images


tagulous.admin.register(Project, ProjectAdmin)
