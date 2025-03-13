from datetime import datetime

import requests
import tagulous.admin
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html
from django.urls import path
from django.conf import settings
from django import forms

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


class FormationAdmin(admin.ModelAdmin):
    pass


tagulous.admin.register(Formation, FormationAdmin)


class MonthYearField(forms.DateField):
    """Custom DateField that accepts 'YYYY-MM' and converts it to 'YYYY-MM-01'."""

    def to_python(self, value):
        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m").date().replace(day=1)
        except ValueError:
            raise forms.ValidationError("Invalid date format. Please use YYYY-MM.")


class MonthYearWidget(forms.DateInput):
    input_type = "month"


class ClassificationAdminForm(forms.ModelForm):
    start_date = MonthYearField(widget=MonthYearWidget(format="%Y-%m"), required=False)
    end_date = MonthYearField(widget=MonthYearWidget(format="%Y-%m"), required=False)

    class Meta:
        model = Certification
        fields = "__all__"


class CertificationAdmin(admin.ModelAdmin):
    form = ClassificationAdminForm
    fieldsets = (
        ("Certification Information", {"fields": ("title", "institution")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "url", "topics")}),
    )


admin.site.register(Certification, CertificationAdmin)


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
