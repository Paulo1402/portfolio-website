import tagulous.admin
from modeltranslation.admin import TranslationAdmin

from app.admin.mixins import TaggedModelAdminCompat
from app.forms.base import BaseStartDateEndDateForm
from app.models import Formation


class FormationAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Formation
        fields = "__all__"


class FormationAdmin(TranslationAdmin, TaggedModelAdminCompat):
    form = FormationAdminForm
    fieldsets = (
        ("Certification Information", {"fields": ("title", "institution")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "topics")}),
    )
    list_display = ("title", "institution", "created_at", "updated_at")


tagulous.admin.register(Formation, FormationAdmin)
