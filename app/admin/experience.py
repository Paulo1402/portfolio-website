import tagulous.admin
from django.contrib import admin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from app.models import Experience
from app.forms.base import BaseStartDateEndDateForm


class ExperienceAdminForm(TranslatableModelForm, BaseStartDateEndDateForm):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceAdmin(TranslatableAdmin):
    form = ExperienceAdminForm
    # fieldsets = (
    #     ("Experience Information", {"fields": ("title", "company")}),
    #     ("Duration", {"fields": ("start_date", "end_date")}),
    #     ("Details", {"fields": ("description", "topics")}),
    # )
    list_display = (
        "title",
        "company",
        "created_at",
        "updated_at",
    )


tagulous.admin.register(Experience, ExperienceAdmin)
