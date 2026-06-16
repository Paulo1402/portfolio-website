import tagulous.admin
from modeltranslation.admin import TranslationAdmin

from app.admin.mixins import TaggedModelAdminCompat
from app.forms.base import BaseStartDateEndDateForm
from app.models import Experience


class ExperienceAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceAdmin(TranslationAdmin, TaggedModelAdminCompat):
    form = ExperienceAdminForm
    fieldsets = (
        ("Experience Information", {"fields": ("title", "company")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "topics")}),
    )
    list_display = ("title", "company", "created_at", "updated_at")


tagulous.admin.register(Experience, ExperienceAdmin)
