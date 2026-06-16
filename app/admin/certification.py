import tagulous.admin
from modeltranslation.admin import TranslationAdmin

from app.admin.mixins import TaggedModelAdminCompat
from app.forms.base import BaseStartDateEndDateForm
from app.models import Certification


class CertificationAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Certification
        fields = "__all__"
        exclude = ("created_at", "updated_at")


class CertificationAdmin(TranslationAdmin, TaggedModelAdminCompat):
    form = CertificationAdminForm
    fieldsets = (
        ("Certification Information", {"fields": ("title", "institution")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "url", "topics")}),
    )
    list_display = ("title", "institution", "created_at", "updated_at")


tagulous.admin.register(Certification, CertificationAdmin)
