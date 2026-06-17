import logging

import tagulous.admin
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from PIL import Image

from app.admin.mixins import TaggedModelAdminCompat
from app.forms.base import BaseStartDateEndDateForm
from app.models import Project, ProjectImage
from app.utils.github import GitHubImportError, import_project_from_github
from app.utils.image import (
    convert_image_to_inmemoryfile,
    get_max_image_dimensions,
    resize_and_pad_image,
)

logger = logging.getLogger(__name__)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectAdmin(TranslationAdmin, TaggedModelAdminCompat):
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

        try:
            result = import_project_from_github(project)
        except GitHubImportError as error:
            self.message_user(
                request,
                str(error),
                level=messages.ERROR,
            )
        except Exception as e:
            logger.exception(
                f"Failed to fetch GitHub data for project {project.id}", exc_info=e
            )
            self.message_user(
                request,
                "Failed to fetch GitHub data.",
                level=messages.ERROR,
            )
        else:
            if result.images_count:
                message = "GitHub data and images updated."
                level = messages.SUCCESS
            else:
                message = "GitHub data updated. No supported images found."
                level = messages.WARNING

            self.message_user(request, message, level=level)

        return redirect("/admin/app/project/")

    def save_model(self, request, obj: Project, form, change):
        super().save_model(request, obj, form, change)

        project_images = obj.project_images.all()
        self.resize_and_pad_images(list(project_images))

    @staticmethod
    def resize_and_pad_images(product_images: list[ProjectImage]):
        if not product_images:
            return

        width, height = get_max_image_dimensions(
            [product_image.image for product_image in product_images]
        )

        for product_image in product_images:
            image = product_image.image
            image_name = image.name
            image.open()  # The image must be open before using Image.open from PIL

            image = Image.open(image)

            resized_image = resize_and_pad_image(image, width, height)
            inmemory_image = convert_image_to_inmemoryfile(
                resized_image, image_name, image_format=image.format
            )

            product_image.image = inmemory_image
            product_image.save()


tagulous.admin.register(Project, ProjectAdmin)
