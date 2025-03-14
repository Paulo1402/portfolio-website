import tagulous.admin
from django.contrib import admin

from app.models import Experience
from app.forms.base import BaseStartDateEndDateForm


class ExperienceAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceAdmin(admin.ModelAdmin):
    form = ExperienceAdminForm
    fieldsets = (
        ("Experience Information", {"fields": ("title", "company")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "topics")}),
    )


tagulous.admin.register(Experience, ExperienceAdmin)
